import * as React from "react";
import { Pressable, ScrollView, StyleSheet, View } from "react-native";
import { Card, ErrorBlock, H2, H3, LoadingBlock, Muted, Screen } from "@/components/ui";
import { ApiError, getPreparationPlanPage, toggleGoal, type PreparationPlanPageOut } from "@/lib/api";
import { colors, spacing } from "@/lib/theme";

/** phase.md Phase 19: reproduces frontend/src/app/PreparationPlanPage.tsx's
 * behavior (same `/students/me/preparation-plan-page` data), including
 * toggling short/long-term goal completion against the same endpoint. */
export default function PreparationPlanScreen() {
  const [data, setData] = React.useState<PreparationPlanPageOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const load = React.useCallback(() => {
    getPreparationPlanPage()
      .then((d) => {
        setData(d);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load your preparation plan." : "Network error.");
      });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  async function handleToggle(goalId: string) {
    const result = await toggleGoal(goalId);
    setData((prev) =>
      prev
        ? { ...prev, short_term_goals: result.short_term_goals, long_term_goals: result.long_term_goals }
        : prev,
    );
  }

  return (
    <Screen>
      <ScrollView contentContainerStyle={styles.content}>
        {!data && !error ? <LoadingBlock label="Loading your preparation plan…" /> : null}
        {error ? <ErrorBlock message={error} /> : null}
        {data ? (
          data.target_company === null ? (
            <Card>
              <H3>No Target Company Set</H3>
              <Muted>Set a target company to generate a preparation plan.</Muted>
            </Card>
          ) : (
            <>
              <H2>Preparation Plan</H2>
              <Muted>
                Target: {data.target_company} — {data.target_role ?? "Any role"}
              </Muted>

              <Card>
                <H3>Readiness</H3>
                {data.readiness.has_analysis ? (
                  <Muted>
                    {data.readiness.readiness_percentage}% — {data.readiness.status_message}
                  </Muted>
                ) : (
                  <Muted>No analysis yet.</Muted>
                )}
              </Card>

              <Card>
                <H3>Year-Wise Focus</H3>
                {data.year_wise_focus.map((y, idx) => (
                  <Muted key={idx}>
                    {y.is_current ? "→ " : ""}
                    {y.year}: {y.focus_text}
                  </Muted>
                ))}
              </Card>

              <GoalCard title="Short-Term Goals" goals={data.short_term_goals} onToggle={handleToggle} />
              <GoalCard title="Long-Term Goals" goals={data.long_term_goals} onToggle={handleToggle} />
            </>
          )
        ) : null}
      </ScrollView>
    </Screen>
  );
}

function GoalCard({
  title,
  goals,
  onToggle,
}: {
  title: string;
  goals: { id: string; text: string; completed: boolean }[];
  onToggle: (id: string) => void;
}) {
  return (
    <Card>
      <H3>{title}</H3>
      {goals.length === 0 ? (
        <Muted>No goals yet.</Muted>
      ) : (
        goals.map((g) => (
          <Pressable key={g.id} style={styles.goalRow} onPress={() => onToggle(g.id)}>
            <View style={[styles.checkbox, g.completed && styles.checkboxChecked]} />
            <Muted>{g.text}</Muted>
          </Pressable>
        ))
      )}
    </Card>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: spacing.lg,
    gap: spacing.md,
  },
  goalRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    paddingVertical: spacing.xs,
  },
  checkbox: {
    width: 18,
    height: 18,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: colors.borderHi,
  },
  checkboxChecked: {
    backgroundColor: colors.accent,
    borderColor: colors.accent,
  },
});
