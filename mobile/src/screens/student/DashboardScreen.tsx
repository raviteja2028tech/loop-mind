import * as React from "react";
import { RefreshControl, ScrollView, StyleSheet, View } from "react-native";
import {
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
import { ApiError, getDashboard, type DashboardData } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { spacing } from "@/lib/theme";

/** phase.md Phase 19: reproduces frontend/src/app/StudentDashboard.tsx's
 * behavior (same `/students/me/dashboard` data) as a native screen. */
export default function DashboardScreen() {
  const { logout } = useAuth();
  const [data, setData] = React.useState<DashboardData | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [refreshing, setRefreshing] = React.useState(false);

  const load = React.useCallback(() => {
    return getDashboard()
      .then((d) => {
        setData(d);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load your dashboard." : "Network error.");
      });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  async function handleRefresh() {
    setRefreshing(true);
    await load();
    setRefreshing(false);
  }

  return (
    <Screen>
      <ScrollView
        contentContainerStyle={styles.content}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />}
      >
        {!data && !error ? <LoadingBlock label="Loading your dashboard…" /> : null}
        {error ? <ErrorBlock message={error} /> : null}
        {data ? (
          <>
            <H2>Welcome back, {data.full_name || "Student"}!</H2>
            <Muted>Manage your hiring journey with AI-powered insights.</Muted>

            <View style={styles.statRow}>
              <StatBlock label="Profile" value={`${data.profile_completion_percentage}%`} accent />
              <StatBlock label="Skills" value={data.skills_count} />
              <StatBlock label="Projects" value={data.projects_count} />
            </View>
            <View style={styles.statRow}>
              <StatBlock label="Certifications" value={data.certifications_count} />
              <StatBlock
                label="Target Company"
                value={data.target_company ?? "Not set"}
              />
            </View>

            <Card>
              <H3>Placement Readiness</H3>
              {data.placement_readiness.has_analysis ? (
                <Muted>
                  {data.placement_readiness.readiness_percentage}% —{" "}
                  {data.placement_readiness.status_message}
                </Muted>
              ) : (
                <Muted>Set a target company on Skill Gap to see your readiness.</Muted>
              )}
            </Card>

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
