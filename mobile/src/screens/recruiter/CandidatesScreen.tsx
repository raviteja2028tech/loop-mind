import * as React from "react";
import { Alert, FlatList, StyleSheet } from "react-native";
import { Badge, Button, Card, ErrorBlock, H3, LoadingBlock, Muted, Screen } from "@/components/ui";
import { approveCandidate, ApiError, getCandidatesPage, type CandidateRow } from "@/lib/api";
import { spacing } from "@/lib/theme";

const STATUS_TONE: Record<string, "ok" | "hold" | "rejected" | "neutral"> = {
  Shortlisted: "ok",
  "Under Review": "hold",
  Rejected: "rejected",
};

/** phase.md Phase 19: a read + Approve-only mobile view of frontend/src/
 * recruiter/CandidatesPage.tsx (same `/recruiters/me/candidates` and the
 * same `/approve` action). The AI Recruitment Workflow's React Flow
 * diagram and Disapprove-with-reason flow stay web-only — React Flow has
 * no native port, and disapproval's free-text reason is a worse fit for a
 * phone keyboard than a deliberate web-side action; phase.md's critical
 * rule is reusing the same backend/business rules, not replicating every
 * desktop interaction. */
export default function RecruiterCandidatesScreen() {
  const [candidates, setCandidates] = React.useState<CandidateRow[] | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const load = React.useCallback(() => {
    getCandidatesPage()
      .then((d) => {
        setCandidates(d.candidates);
        setError(null);
      })
      .catch((err) => setError(err instanceof ApiError ? "Could not load candidates." : "Network error."));
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  async function handleApprove(applicationId: number) {
    try {
      await approveCandidate(applicationId);
      load();
      Alert.alert("Approved", "Candidate approved and moved forward in the workflow.");
    } catch {
      Alert.alert("Error", "Could not approve this candidate.");
    }
  }

  return (
    <Screen>
      {!candidates && !error ? <LoadingBlock label="Loading candidates…" /> : null}
      {error ? <ErrorBlock message={error} /> : null}
      {candidates ? (
        <FlatList
          contentContainerStyle={styles.content}
          data={candidates}
          keyExtractor={(c) => String(c.application_id)}
          ListEmptyComponent={<Muted>No candidates yet.</Muted>}
          renderItem={({ item }) => (
            <Card>
              <H3>{item.candidate_name}</H3>
              <Muted>
                {item.job_title} · {item.applied_role}
              </Muted>
              <Muted>AI Score: {item.ai_score ?? "—"}/100</Muted>
              <Badge label={item.status_label} tone={STATUS_TONE[item.status_label] ?? "neutral"} />
              {item.status_label !== "Shortlisted" ? (
                <Button title="Approve" onPress={() => handleApprove(item.application_id)} />
              ) : null}
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
