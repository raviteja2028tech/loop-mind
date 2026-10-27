import * as React from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import { Badge, Card, ErrorBlock, H2, H3, LoadingBlock, Muted, Screen, StatBlock } from "@/components/ui";
import { ApiError, getSkillGapPage, type SkillGapPageOut } from "@/lib/api";
import { spacing } from "@/lib/theme";

const STATUS_TONE: Record<string, "ok" | "hold" | "rejected" | "neutral"> = {
  Strong: "ok",
  "To Improve": "hold",
  Missing: "rejected",
  "Not Relevant": "neutral",
};

/** phase.md Phase 19: reproduces frontend/src/app/SkillGapAnalysis.tsx's
 * behavior (same `/students/me/skill-gap` data). */
export default function SkillGapScreen() {
  const [data, setData] = React.useState<SkillGapPageOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getSkillGapPage()
      .then((d) => {
        setData(d);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load skill gap analysis." : "Network error.");
      });
  }, []);

  return (
    <Screen>
      <ScrollView contentContainerStyle={styles.content}>
        {!data && !error ? <LoadingBlock label="Loading your skill gap analysis…" /> : null}
        {error ? <ErrorBlock message={error} /> : null}
        {data ? (
          data.target_company === null ? (
            <Card>
              <H3>No Target Company Set</H3>
              <Muted>
                Set a target company from the Student Dashboard on the web app to see your skill
                gap analysis here.
              </Muted>
            </Card>
          ) : (
            <>
              <H2>Skill Gap Analysis</H2>
              <Muted>
                Target: {data.target_company} — {data.target_role ?? "Any role"}
              </Muted>

              <Card>
                <H3>Readiness</H3>
                {data.readiness.has_analysis ? (
                  <>
                    <Muted>{data.readiness.readiness_percentage}% ready</Muted>
                    <Muted>{data.readiness.status_message}</Muted>
                  </>
                ) : (
                  <Muted>No analysis yet.</Muted>
                )}
              </Card>

              <View style={styles.statRow}>
                <StatBlock label="Required" value={data.overview.total_required_skills} />
                <StatBlock label="You Have" value={data.overview.skills_you_have} accent />
                <StatBlock label="To Improve" value={data.overview.skills_to_improve} />
              </View>

              <Card>
                <H3>Priority Areas</H3>
                {data.priority_areas.length === 0 ? (
                  <Muted>No priority gaps right now.</Muted>
                ) : (
                  data.priority_areas.map((p) => (
                    <Muted key={p.rank}>
                      {p.rank}. {p.skill} — {p.impact}
                    </Muted>
                  ))
                )}
              </Card>

              <Card>
                <H3>Skills</H3>
                {data.skills.map((s, idx) => (
                  <View key={idx} style={styles.skillRow}>
                    <View style={{ flex: 1 }}>
                      <Muted>
                        {s.skill} ({s.category})
                      </Muted>
                      <Muted>
                        Your level: {s.your_level} · Required: {s.required_level}
                      </Muted>
                    </View>
                    <Badge label={s.status} tone={STATUS_TONE[s.status] ?? "neutral"} />
                  </View>
                ))}
              </Card>
            </>
          )
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
  skillRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    paddingVertical: spacing.xs,
  },
});
