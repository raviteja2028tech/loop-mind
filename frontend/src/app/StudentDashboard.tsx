import * as React from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, XAxis, YAxis } from "recharts";
import {
  Button,
  Card,
  ChartTooltip,
  ChartWell,
  Dropzone,
  ErrorState,
  GlobalFooter,
  LoadingState,
  Modal,
  StudentNavbar,
  Progress,
  ReadinessRing,
  SearchableSelect,
  Shell,
  SimpleSelect,
  StatCard,
} from "@/components";
import {
  type DashboardData,
  type PlacementReadinessDetail,
  ApiError,
  getCompanyOptions,
  getDashboard,
  getPlacementReadinessDetail,
  putTargetCompany,
  uploadResume,
} from "@/lib/api";

function TargetCompanyModal({
  open,
  onOpenChange,
  onSaved,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSaved: (companyName: string) => void;
}) {
  const [options, setOptions] = React.useState<string[]>([]);
  const [selected, setSelected] = React.useState<string | null>(null);
  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (!open) return;
    getCompanyOptions()
      .then((rows) => {
        setOptions(rows.map((r) => r.name));
        setError(null);
      })
      .catch(() => setError("Could not load companies. Please try again."));
  }, [open]);

  async function handleSave() {
    if (!selected) return;
    setSaving(true);
    setError(null);
    try {
      await putTargetCompany(selected);
      onSaved(selected);
      onOpenChange(false);
    } catch {
      setError("Could not save your target company. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Set Target Company">
      <div className="flex flex-col gap-4">
        <SearchableSelect
          options={options.map((name) => ({ value: name, label: name }))}
          value={selected}
          onChange={setSelected}
          placeholder="Select a company…"
          searchPlaceholder="Search companies…"
        />
        {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
        <Button onClick={handleSave} disabled={!selected || saving} className="self-end">
          {saving ? "Saving…" : "Save"}
        </Button>
      </div>
    </Modal>
  );
}

/** Student Dashboard UPDATE SDD §10-12: "View Detailed Analysis" opens a
 * centered modal on the same dashboard page (no navigation away),
 * live-fetching from the Placement Readiness Agent every time it opens
 * so it always reflects the student's current stored evidence. */
function PlacementReadinessModal({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Placement Readiness — Detailed Analysis">
      {/* Mounted fresh every time the modal opens, so its state always
       * starts empty and the fetch below always reflects the student's
       * latest stored data — no stale result briefly shown while it
       * reloads. */}
      {open ? <PlacementReadinessModalContent /> : null}
    </Modal>
  );
}

function PlacementReadinessModalContent() {
  const [detail, setDetail] = React.useState<PlacementReadinessDetail | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getPlacementReadinessDetail()
      .then(setDetail)
      .catch(() => setError("Could not load your placement readiness analysis."));
  }, []);

  return (
    <>
      {error ? <ErrorState message={error} /> : null}
      {!detail && !error ? <LoadingState label="Analyzing your current profile…" /> : null}
      {detail && !detail.has_analysis ? (
        <p className="text-sm text-[var(--text-mute)]">
          Set a target company on your dashboard to see a detailed placement readiness analysis.
        </p>
      ) : null}
      {detail?.has_analysis ? (
        <div className="flex flex-col gap-4">
          <div>
            <p className="text-sm text-[var(--text-mute)]">
              Target: <span className="text-[var(--text)]">{detail.target_company}</span>
              {detail.target_role ? ` — ${detail.target_role}` : ""}
            </p>
            <p className="mt-1 font-medium text-[var(--text)]">{detail.status_message}</p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-[var(--text)]">
              Ready Skills ({detail.ready_skills.length})
            </h4>
            <p className="text-xs text-[var(--text-mute)]">
              Skills where you currently meet or exceed what {detail.target_company} expects
              {detail.target_role ? ` for ${detail.target_role}` : ""}.
            </p>
            {detail.ready_skills.length === 0 ? (
              <p className="mt-2 text-sm text-[var(--text-mute)]">
                No skills currently meet the required level yet.
              </p>
            ) : (
              <ul className="mt-2 flex flex-wrap gap-2">
                {detail.ready_skills.map((name) => (
                  <li
                    key={name}
                    className="rounded-full border border-[var(--accent)] px-3 py-1 text-xs text-[var(--accent)]"
                  >
                    {name}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div>
            <h4 className="text-sm font-semibold text-[var(--text)]">
              Current Skills ({detail.current_skills.length})
            </h4>
            {detail.current_skills.length === 0 ? (
              <p className="text-sm text-[var(--text-mute)]">No skills added yet.</p>
            ) : (
              <ul className="mt-2 flex flex-col gap-1">
                {detail.current_skills.map((s) => (
                  <li
                    key={s.skill_name}
                    className="flex items-center justify-between text-sm text-[var(--text-soft)]"
                  >
                    <span>{s.skill_name}</span>
                    <span className="text-xs text-[var(--text-mute)]">
                      {s.proficiency} · {s.evidence_count} evidence
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      ) : null}
    </>
  );
}

/** Skill Gap, Profile Photo & Resume Management Update SDD §11-12: this
 * card no longer disappears once a resume exists — it stays in the same
 * area as Placement Readiness/Target Company/Recent Activity and simply
 * reflects the current resume state ("Upload" vs. "Resume Available /
 * Replace"), so the student always has a path to manage their resume
 * from the Dashboard, not just from My Profile. Uploading/replacing here
 * goes through the exact same `/students/me/resume` endpoint as My
 * Profile and the Professional Links onboarding step — the same Resume
 * Parser Agent extraction, never a second/duplicate resume record. */
function UploadResumeCard({
  hasResume,
  onUploaded,
}: {
  hasResume: boolean;
  onUploaded: () => void;
}) {
  const [uploading, setUploading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function handleFiles(files: File[]) {
    const file = files[0];
    if (!file) return;
    const isPdf = file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
    if (!isPdf) {
      setError("Resume must be a PDF file.");
      return;
    }
    setUploading(true);
    setError(null);
    try {
      await uploadResume(file);
      onUploaded();
    } catch {
      setError("Could not upload resume. Please try again.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <Card>
      <h3>{hasResume ? "Resume Available" : "Upload Your Resume"}</h3>
      <p className="text-sm text-[var(--text-mute)]">
        {hasResume
          ? "Replace it with an updated version any time — skills, projects and certifications are re-extracted automatically."
          : "Add your resume to automatically fill in skills, projects, and certifications."}
      </p>
      <Dropzone
        accept="application/pdf"
        onFiles={handleFiles}
        hint={
          uploading
            ? "Uploading…"
            : hasResume
              ? "Replace resume (PDF)"
              : "Upload your resume as a PDF"
        }
      />
      {error ? <ErrorState message={error} /> : null}
    </Card>
  );
}

export default function StudentDashboard() {
  const [dashboard, setDashboard] = React.useState<DashboardData | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [modalOpen, setModalOpen] = React.useState(false);
  const [readinessModalOpen, setReadinessModalOpen] = React.useState(false);

  const load = React.useCallback(() => {
    getDashboard()
      .then((data) => {
        setDashboard(data);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load your dashboard." : "Network error.");
      });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  return (
    <Shell navbar={<StudentNavbar />} footer={<GlobalFooter />}>
      {!dashboard && !error ? <LoadingState label="Loading your dashboard…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {dashboard ? (
        <DashboardBody
          dashboard={dashboard}
          onOpenTargetCompanyModal={() => setModalOpen(true)}
          onTargetCompanySaved={() => load()}
          onOpenReadinessModal={() => setReadinessModalOpen(true)}
          onResumeUploaded={() => load()}
        />
      ) : null}
      <TargetCompanyModal open={modalOpen} onOpenChange={setModalOpen} onSaved={() => load()} />
      <PlacementReadinessModal open={readinessModalOpen} onOpenChange={setReadinessModalOpen} />
    </Shell>
  );
}

function DashboardBody({
  dashboard,
  onOpenTargetCompanyModal,
  onOpenReadinessModal,
  onResumeUploaded,
}: {
  dashboard: DashboardData;
  onOpenTargetCompanyModal: () => void;
  onTargetCompanySaved: () => void;
  onOpenReadinessModal: () => void;
  onResumeUploaded: () => void;
}) {
  const readiness = dashboard.placement_readiness;

  return (
    <>
      {/* Header / Welcome */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
        <div>
          <h2>Hello, {dashboard.full_name}!</h2>
          <p className="mt-1 text-sm text-[var(--text-soft)]">
            Keep learning, keep building. You’re one step closer to your dream career.
          </p>
        </div>
        <Card flat className="justify-center text-center">
          <p className="text-sm text-[var(--text-soft)] italic">
            “A year from now, you’ll wish you had started today.”
          </p>
          <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
        </Card>
      </div>

      {/* Top summary cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <StatCard
            label="Profile Completion"
            value={`${dashboard.profile_completion_percentage}%`}
            accent
          />
          <Progress value={dashboard.profile_completion_percentage} />
        </Card>
        <Card>
          <StatCard label="Current Skills" value={dashboard.skills_count} />
        </Card>
        <Card>
          <StatCard label="Projects" value={dashboard.projects_count} />
        </Card>
        <Card>
          <StatCard label="Certifications" value={dashboard.certifications_count} />
        </Card>
      </div>

      {/* Main insight row */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card>
          <h3>Placement Readiness</h3>
          {readiness.has_analysis ? (
            <>
              <div className="flex items-center gap-4">
                <ReadinessRing percentage={readiness.readiness_percentage ?? 0} />
                <div>
                  <p className="font-medium text-[var(--text)]">{readiness.status_message}</p>
                  <p className="text-sm text-[var(--text-mute)]">
                    Keep improving your skills and adding more evidence to boost your placement
                    readiness.
                  </p>
                </div>
              </div>
              <Button variant="ghost" onClick={onOpenReadinessModal} className="self-start">
                View Detailed Analysis →
              </Button>
            </>
          ) : (
            <>
              <p className="text-sm text-[var(--text-mute)]">
                Complete your profile and run a Skill Gap Analysis to see your placement readiness
                here.
              </p>
              <Button variant="ghost" onClick={onOpenReadinessModal} className="self-start">
                View Detailed Analysis →
              </Button>
            </>
          )}
        </Card>

        <Card>
          <h3>Target Company</h3>
          {dashboard.target_company ? (
            <p className="text-lg font-semibold text-[var(--accent)]">{dashboard.target_company}</p>
          ) : (
            <>
              <p className="text-[var(--text-mute)]">Not set yet</p>
              <p className="text-sm text-[var(--text-mute)]">
                Set a target company to get personalized recommendations, skill analysis and
                preparation plan.
              </p>
              <Button variant="ghost" onClick={onOpenTargetCompanyModal} className="self-start">
                Set Target Company →
              </Button>
            </>
          )}
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <h3>Recent Activity</h3>
            <Button variant="ghost" disabled className="!px-2 !py-1 text-xs">
              View All
            </Button>
          </div>
          {dashboard.recent_activity.length === 0 ? (
            <p className="text-sm text-[var(--text-mute)]">No activity yet.</p>
          ) : (
            <ul className="flex flex-col gap-2">
              {dashboard.recent_activity.map((item, idx) => (
                <li key={idx} className="flex items-baseline justify-between gap-3 text-sm">
                  <span className="text-[var(--text-soft)]">
                    {item.label}
                    {item.detail ? (
                      <span className="text-[var(--text-mute)]"> · {item.detail}</span>
                    ) : null}
                  </span>
                  <span className="shrink-0 text-xs text-[var(--text-mute)]">
                    {item.relative_time}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <UploadResumeCard hasResume={dashboard.has_resume} onUploaded={onResumeUploaded} />
      </div>

      {/* Progress / task row */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[2fr_1fr]">
        <Card>
          <h3>Your Preparation Journey</h3>
          <p className="text-sm text-[var(--text-mute)]">
            Track your progress across key milestones.
          </p>
          <div className="mt-2 flex items-center">
            {dashboard.preparation_journey.map((stage, idx) => (
              <React.Fragment key={stage.key}>
                {idx > 0 ? (
                  <div
                    className="mx-1 h-px flex-1"
                    style={{
                      background: stage.complete ? "var(--accent)" : "var(--border)",
                    }}
                  />
                ) : null}
                <div className="flex flex-col items-center gap-1.5 text-center">
                  <div
                    className="flex size-8 items-center justify-center rounded-full text-xs font-semibold"
                    style={{
                      background: stage.complete ? "var(--accent)" : "var(--raised)",
                      color: stage.complete ? "var(--bg)" : "var(--text-mute)",
                      border: stage.complete ? "none" : "1px solid var(--border-hi)",
                    }}
                  >
                    {stage.complete ? "✓" : idx + 1}
                  </div>
                  <span className="text-xs font-medium text-[var(--text)]">{stage.label}</span>
                  <span className="text-[11px] text-[var(--text-mute)]">
                    {stage.supporting_text}
                  </span>
                </div>
              </React.Fragment>
            ))}
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <h3>Upcoming Tasks</h3>
            <Button variant="ghost" disabled className="!px-2 !py-1 text-xs">
              View all
            </Button>
          </div>
          {dashboard.upcoming_tasks.length === 0 ? (
            <p className="text-sm text-[var(--text-mute)]">You’re all caught up!</p>
          ) : (
            <ul className="flex flex-col gap-2">
              {dashboard.upcoming_tasks.map((task, idx) => (
                <li key={idx} className="flex items-center gap-2 text-sm text-[var(--text-soft)]">
                  <span
                    className="inline-block size-3.5 shrink-0 rounded-sm"
                    style={{ border: "1px solid var(--border-hi)" }}
                  />
                  {task.label}
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>

      {/* Recommendation / statistics row */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[2fr_1fr]">
        <Card>
          <h3>Recommended for You</h3>
          <p className="text-sm text-[var(--text-mute)]">
            Based on your current progress and goals.
          </p>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {dashboard.recommended_for_you.map((rec, idx) => (
              <div
                key={idx}
                className="flex flex-col gap-1 rounded-[var(--radius)] border border-[var(--border)] bg-[var(--raised)] p-3"
              >
                <span className="text-sm font-medium text-[var(--text)]">{rec.title}</span>
                <span className="text-xs text-[var(--text-mute)]">{rec.type}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <h3>Your Stats</h3>
            <SimpleSelect
              options={[{ value: "30d", label: "Last 30 days" }]}
              value="30d"
              disabled
              className="!w-auto text-xs"
              onChange={() => {}}
            />
          </div>
          <ChartWell>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={dashboard.stats}>
                <CartesianGrid vertical={false} />
                <XAxis dataKey="category" tickLine={false} axisLine={false} />
                <YAxis allowDecimals={false} tickLine={false} axisLine={false} width={28} />
                <ChartTooltip />
                <Bar dataKey="value" fill="var(--accent)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartWell>
        </Card>
      </div>
    </>
  );
}
