import * as React from "react";
import { FlatList, StyleSheet } from "react-native";
import { Badge, Card, ErrorBlock, H3, LoadingBlock, Muted, Screen } from "@/components/ui";
import { ApiError, getRecruiterJobsPage, type RecruiterJobRow } from "@/lib/api";
import { spacing } from "@/lib/theme";

/** phase.md Phase 19: a read-only mobile view of frontend/src/recruiter/
 * JobManagementPage.tsx's job list (same `/recruiters/me/jobs`). Creating
 * a job stays a web-only action in this pass — a multi-field form (job
 * title, role, experience, skill tags) is a worse fit for a phone screen
 * than the recruiter's desktop workflow, and nothing in phase.md requires
 * replicating every desktop action on mobile. */
export default function RecruiterJobsScreen() {
  const [jobs, setJobs] = React.useState<RecruiterJobRow[] | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getRecruiterJobsPage()
      .then((d) => {
        setJobs(d.jobs);
        setError(null);
      })
      .catch((err) => setError(err instanceof ApiError ? "Could not load your jobs." : "Network error."));
  }, []);

  return (
    <Screen>
      {!jobs && !error ? <LoadingBlock label="Loading your jobs…" /> : null}
      {error ? <ErrorBlock message={error} /> : null}
      {jobs ? (
        <FlatList
          contentContainerStyle={styles.content}
          data={jobs}
          keyExtractor={(j) => String(j.id)}
          ListEmptyComponent={<Muted>No job postings yet — create one from the web app.</Muted>}
          renderItem={({ item }) => (
            <Card>
              <H3>{item.job_title}</H3>
              <Muted>
                {item.job_role} · {item.experience_required}
              </Muted>
              <Muted>
                {item.applications} applications · {item.shortlisted} shortlisted ·{" "}
                {item.under_review} under review · {item.rejected} rejected
              </Muted>
              <Badge label={item.status === "active" ? "Active" : "Paused"} tone={item.status === "active" ? "ok" : "neutral"} />
            </Card>
          )}
        />
      ) : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: spacing.lg,
    gap: spacing.md,
  },
});
