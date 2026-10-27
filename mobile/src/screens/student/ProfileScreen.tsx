import * as React from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import { Badge, Button, Card, ErrorBlock, H2, H3, LoadingBlock, Muted, Screen } from "@/components/ui";
import {
  ApiError,
  getProfilePage,
  getRecruitmentHistory,
  listSkills,
  type ProfilePageData,
  type RecruitmentHistory,
  type StudentSkill,
} from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { spacing } from "@/lib/theme";

/** phase.md Phase 19 "student profile": a mobile-appropriate read view of
 * My Profile (phase.md Phase 18) against the same `/students/me/profile`,
 * `/students/me/skills` and `/students/me/recruitment-history` endpoints
 * — Overview, Skills and Recruitment History, the three sections that
 * translate most naturally to a single scrolling screen rather than the
 * web's 12-item sidebar. Full editing of every section (Academics, Career
 * & Placement, Consent, ...) stays a web-only surface for now rather than
 * squeezing twelve desktop forms onto a phone in this pass. */
export default function ProfileScreen() {
  const { logout } = useAuth();
  const [page, setPage] = React.useState<ProfilePageData | null>(null);
  const [skills, setSkills] = React.useState<StudentSkill[] | null>(null);
  const [history, setHistory] = React.useState<RecruitmentHistory | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    Promise.all([getProfilePage(), listSkills(), getRecruitmentHistory()])
      .then(([p, s, h]) => {
        setPage(p);
        setSkills(s);
        setHistory(h);
        setError(null);
      })
      .catch((err) => setError(err instanceof ApiError ? "Could not load your profile." : "Network error."));
  }, []);

  return (
    <Screen>
      <ScrollView contentContainerStyle={styles.content}>
        {!page && !error ? <LoadingBlock label="Loading your profile…" /> : null}
        {error ? <ErrorBlock message={error} /> : null}
        {page ? (
          <>
            <H2>{page.overview.full_name ?? "My Profile"}</H2>
            <Muted>
              {page.overview.degree ?? "—"} · {page.overview.college ?? "—"}
            </Muted>
            <Muted>
              {[page.overview.city, page.overview.state].filter(Boolean).join(", ") || "—"}
            </Muted>

            <Card>
              <H3>Profile Completion</H3>
              <Muted>{page.completion_percentage}% complete</Muted>
              {page.missing_fields.length > 0 ? (
                <Muted>
                  Missing: {page.missing_fields.map((m) => m.section).join(", ")}
                </Muted>
              ) : (
                <Muted>Your profile is fully complete.</Muted>
              )}
            </Card>

            <View style={styles.statRow}>
              <Card style={{ flex: 1 }}>
                <Muted>Skills</Muted>
                <H3>{page.stats.skills_added}</H3>
              </Card>
              <Card style={{ flex: 1 }}>
                <Muted>Projects</Muted>
                <H3>{page.stats.projects}</H3>
              </Card>
              <Card style={{ flex: 1 }}>
                <Muted>Certifications</Muted>
                <H3>{page.stats.certifications}</H3>
              </Card>
            </View>

            <Card>
              <H3>Skills</H3>
              {!skills || skills.length === 0 ? (
                <Muted>No skills added yet — add some from the web app.</Muted>
              ) : (
                skills.map((s) => (
                  <Muted key={s.id}>
                    {s.skill_name} — {s.proficiency} ({s.learning_status})
                  </Muted>
                ))
              )}
            </Card>

            <Card>
              <H3>Recruitment History</H3>
              {!history || history.total_applications === 0 ? (
                <Muted>No applications yet.</Muted>
              ) : (
                <>
                  <Muted>
                    {history.total_applications} application(s) · {history.selected_count} selected ·{" "}
                    {history.rejected_count} rejected
                  </Muted>
                  {history.applications.map((a, idx) => (
                    <View key={idx} style={styles.historyRow}>
                      <Muted>
                        {a.company_name} — {a.job_role}
                      </Muted>
                      <Badge
                        label={a.recruitment_stage_reached}
                        tone={a.outcome === "Hired" ? "ok" : a.outcome ? "rejected" : "hold"}
                      />
                    </View>
                  ))}
                </>
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
  historyRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: spacing.xs,
  },
});
