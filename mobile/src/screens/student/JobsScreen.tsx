import * as React from "react";
import { Alert, FlatList, StyleSheet, View } from "react-native";
import {
  Badge,
  Button,
  Card,
  ErrorBlock,
  H2,
  H3,
  LoadingBlock,
  Muted,
  Screen,
  StatBlock,
} from "@/components/ui";
import {
  ApiError,
  applyToJob,
  getJobsPage,
  getMyApplications,
  toggleSaveJob,
  type Application,
  type JobCard,
  type JobsPageOut,
} from "@/lib/api";
import { spacing } from "@/lib/theme";

/** phase.md Phase 19: reproduces frontend/src/app/JobsPage.tsx's behavior
 * (same `/students/me/jobs` browse/apply/save + `/students/me/jobs/
 * applications` My Applications view) against the same backend. */
export default function JobsScreen() {
  const [view, setView] = React.useState<"browse" | "applications">("browse");
  const [page, setPage] = React.useState<JobsPageOut | null>(null);
  const [applications, setApplications] = React.useState<Application[] | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const loadJobs = React.useCallback(() => {
    getJobsPage()
      .then((d) => {
        setPage(d);
        setError(null);
      })
      .catch((err) => setError(err instanceof ApiError ? "Could not load jobs." : "Network error."));
  }, []);

  React.useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  React.useEffect(() => {
    if (view === "applications") {
      getMyApplications().then(setApplications);
    }
  }, [view]);

  async function handleApply(jobId: number) {
    try {
      await applyToJob(jobId);
      loadJobs();
      Alert.alert("Applied", "Your application has been submitted.");
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        const body = err.body as { detail?: { missing?: { label: string; reason: string }[] } };
        const missing = body.detail?.missing ?? [];
        Alert.alert(
          "Missing Information",
          missing.map((m) => `${m.label}: ${m.reason}`).join("\n") ||
            "Complete your profile before applying.",
        );
      } else {
        Alert.alert("Error", "Could not submit your application.");
      }
    }
  }

  async function handleSave(jobId: number) {
    await toggleSaveJob(jobId);
    loadJobs();
  }

  return (
    <Screen>
      <View style={styles.tabs}>
        <Button
          title="Browse Jobs"
          variant={view === "browse" ? "primary" : "ghost"}
          onPress={() => setView("browse")}
        />
        <Button
          title="My Applications"
          variant={view === "applications" ? "primary" : "ghost"}
          onPress={() => setView("applications")}
        />
      </View>

      {error ? <ErrorBlock message={error} /> : null}

      {view === "browse" ? (
        !page ? (
          <LoadingBlock label="Loading jobs…" />
        ) : (
          <FlatList
            contentContainerStyle={styles.content}
            data={page.jobs}
            keyExtractor={(j) => String(j.id)}
            ListHeaderComponent={
              <View style={styles.statRow}>
                <StatBlock label="Total Jobs" value={page.summary.total_jobs} />
                <StatBlock label="Applied" value={page.summary.applied} />
                <StatBlock label="Shortlisted" value={page.summary.shortlisted} accent />
              </View>
            }
            renderItem={({ item }) => (
              <JobRow job={item} onApply={handleApply} onSave={handleSave} />
            )}
          />
        )
      ) : !applications ? (
        <LoadingBlock label="Loading your applications…" />
      ) : (
        <FlatList
          contentContainerStyle={styles.content}
          data={applications}
          keyExtractor={(a) => String(a.id)}
          ListEmptyComponent={<Muted>You haven't applied to any jobs yet.</Muted>}
          renderItem={({ item }) => (
            <Card>
              <H3>{item.job_title}</H3>
              <Muted>
                {item.company_name} · {item.job_role}
              </Muted>
              <Badge
                label={item.status_label}
                tone={item.status_label === "Disapproved" ? "rejected" : "hold"}
              />
              {item.disapproval_reason ? <Muted>Reason: {item.disapproval_reason}</Muted> : null}
            </Card>
          )}
        />
      )}
    </Screen>
  );
}

function JobRow({
  job,
  onApply,
  onSave,
}: {
  job: JobCard;
  onApply: (id: number) => void;
  onSave: (id: number) => void;
}) {
  return (
    <Card>
      <H3>{job.job_title}</H3>
      <Muted>
        {job.company_name} · {job.job_role} · {job.location ?? "Remote"}
      </Muted>
      <Muted>{job.posted_relative}</Muted>
      <View style={styles.actionsRow}>
        <Button
          title={job.has_applied ? "Applied" : "Apply"}
          onPress={() => onApply(job.id)}
          disabled={job.has_applied}
        />
        <Button
          title={job.is_saved ? "Saved" : "Save"}
          variant="ghost"
          onPress={() => onSave(job.id)}
        />
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  tabs: {
    flexDirection: "row",
    gap: spacing.sm,
    padding: spacing.lg,
    paddingBottom: 0,
  },
  content: {
    padding: spacing.lg,
    gap: spacing.md,
  },
  statRow: {
    flexDirection: "row",
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  actionsRow: {
    flexDirection: "row",
    gap: spacing.sm,
  },
});
