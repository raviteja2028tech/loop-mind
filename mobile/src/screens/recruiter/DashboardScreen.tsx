import * as React from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import { Button, Card, ErrorBlock, H2, H3, LoadingBlock, Muted, Screen } from "@/components/ui";
import { ApiError, getRecruiterDashboard, type RecruiterDashboardData } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { spacing } from "@/lib/theme";

/** phase.md Phase 19: a read-only mobile view of frontend/src/recruiter/
 * RecruiterDashboard.tsx's statistics (same `/recruiters/me/dashboard`). */
export default function RecruiterDashboardScreen() {
  const { logout } = useAuth();
  const [data, setData] = React.useState<RecruiterDashboardData | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getRecruiterDashboard()
      .then((d) => {
        setData(d);
        setError(null);
      })
      .catch((err) => setError(err instanceof ApiError ? "Could not load your dashboard." : "Network error."));
  }, []);

  return (
    <Screen>
      <ScrollView contentContainerStyle={styles.content}>
        {!data && !error ? <LoadingBlock label="Loading your dashboard…" /> : null}
        {error ? <ErrorBlock message={error} /> : null}
        {data ? (
          <>
            <H2>Recruiter Dashboard</H2>
            <Muted>Manage your hiring process on the go.</Muted>

            <View style={styles.statRow}>
              <Card style={{ flex: 1 }}>
                <Muted>Total Jobs</Muted>
                <H3>{data.summary.total_jobs}</H3>
              </Card>
              <Card style={{ flex: 1 }}>
                <Muted>Applications</Muted>
                <H3>{data.summary.total_applications}</H3>
              </Card>
            </View>
            <View style={styles.statRow}>
              <Card style={{ flex: 1 }}>
                <Muted>Shortlisted</Muted>
                <H3>{data.summary.shortlisted}</H3>
              </Card>
              <Card style={{ flex: 1 }}>
                <Muted>Under Review</Muted>
                <H3>{data.summary.under_review}</H3>
              </Card>
            </View>

            <Card>
              <H3>Recent Activity</H3>
              {data.recent_activity.length === 0 ? (
                <Muted>No activity yet.</Muted>
              ) : (
                data.recent_activity.map((item, idx) => (
                  <Muted key={idx}>
                    {item.label}
                    {item.detail ? ` — ${item.detail}` : ""} · {item.relative_time}
                  </Muted>
                ))
              )}
            </Card>

            <Button title="Log Out" variant="ghost" onPress={logout} />
          </>
        ) : null}
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: spacing.lg,
    gap: spacing.md,
  },
  statRow: {
    flexDirection: "row",
    gap: spacing.sm,
  },
});
