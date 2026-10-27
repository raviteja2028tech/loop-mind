import * as React from "react";
import {
  Badge,
  Button,
  Card,
  ErrorState,
  Input,
  LoadingState,
  Modal,
  RecruiterNavbar,
  Shell,
  SimpleSelect,
  StatCard,
  Textarea,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import {
  ApiError,
  getInterviewDetail,
  getInterviewsPage,
  scheduleInterview,
  setInterviewOutcome,
  setInterviewStatus,
  type InterviewDetail,
  type InterviewRow,
  type InterviewsPageData,
} from "@/lib/api";
import { RecruiterFooter } from "@/recruiter/RecruiterFooter";

const INTERVIEW_TYPES = ["Technical", "HR", "Managerial"];

const STATUS_BADGE: Record<string, "ok" | "hold" | "rejected" | "neutral"> = {
  Scheduled: "hold",
  Completed: "ok",
  Cancelled: "rejected",
  Pending: "neutral",
};

const EMAIL_STATUS_BADGE: Record<string, "ok" | "hold" | "rejected" | "neutral"> = {
  sent: "ok",
  sending: "hold",
  failed: "rejected",
  pending: "neutral",
};

const EMAIL_SOURCE_LABEL: Record<string, string> = {
  profile: "profile email",
  resume: "resume-extracted email",
  unavailable: "unavailable",
};

export default function InterviewsPage() {
  const [page, setPage] = React.useState<InterviewsPageData | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [search, setSearch] = React.useState("");
  const [jobId, setJobId] = React.useState("all");
  const [status, setStatus] = React.useState("all");
  const [scheduleOpen, setScheduleOpen] = React.useState(false);
  const [detailApplicationId, setDetailApplicationId] = React.useState<number | null>(null);
  const [outcomeApplicationId, setOutcomeApplicationId] = React.useState<number | null>(null);

  const load = React.useCallback(() => {
    getInterviewsPage()
      .then((data) => {
        setPage(data);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load interviews." : "Network error.");
      });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const filteredInterviews = React.useMemo(() => {
    if (!page) return [];
    let rows = page.interviews;
    if (jobId !== "all") rows = rows.filter((r) => r.job_id === Number(jobId));
    if (status !== "all") rows = rows.filter((r) => r.status_label === status);
    const needle = search.trim().toLowerCase();
    if (needle) {
      rows = rows.filter(
        (r) =>
          r.candidate_name.toLowerCase().includes(needle) ||
          r.job_role.toLowerCase().includes(needle),
      );
    }
    return rows;
  }, [page, search, jobId, status]);

  async function handleSetStatus(row: InterviewRow, next: "completed" | "cancelled") {
    await setInterviewStatus(row.application_id, next);
    load();
  }

  const columns: Column<InterviewRow & { id: number }>[] = [
    { key: "candidate_name", header: "Candidate Name", render: (r) => r.candidate_name },
    { key: "job_role", header: "Job Role", render: (r) => r.job_role },
    { key: "interview_type", header: "Interview Type", render: (r) => r.interview_type ?? "—" },
    {
      key: "scheduled_at",
      header: "Date & Time",
      render: (r) => r.scheduled_at_display ?? "—",
    },
    {
      key: "ai_status",
      header: "AI Status",
      render: (r) => <Badge variant="hold">{r.ai_status_label}</Badge>,
    },
    {
      key: "status",
      header: "Status",
      render: (r) => (
        <div className="flex flex-col gap-1">
          <Badge variant={STATUS_BADGE[r.status_label] ?? "neutral"}>{r.status_label}</Badge>
          {r.outcome_label ? (
            <Badge variant={r.outcome_label === "Hired" ? "ok" : "rejected"}>
              {r.outcome_label}
            </Badge>
          ) : null}
        </div>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            className="!px-2 !py-1 text-xs"
            onClick={() => setDetailApplicationId(r.application_id)}
          >
            View Questions →
          </Button>
          {r.status_label === "Scheduled" ? (
            <>
              <Button
                variant="ghost"
                className="!px-2 !py-1 text-xs"
                onClick={() => handleSetStatus(r, "completed")}
              >
                Mark Completed
              </Button>
              <Button
                variant="danger"
                className="!px-2 !py-1 text-xs"
                onClick={() => handleSetStatus(r, "cancelled")}
              >
                Cancel
              </Button>
            </>
          ) : null}
          {r.status_label === "Completed" && !r.outcome_label ? (
            <Button
              className="!px-2 !py-1 text-xs"
              onClick={() => setOutcomeApplicationId(r.application_id)}
            >
              Record Outcome →
            </Button>
          ) : null}
        </div>
      ),
    },
  ];

  return (
    <Shell
      navbar={<RecruiterNavbar />}
      footer={<RecruiterFooter />}
    >
      {!page && !error ? <LoadingState label="Loading interviews…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {page ? (
        <>
          {/* Header */}
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
            <div>
              <h2>Interviews</h2>
              <p className="mt-1 text-sm text-[var(--text-soft)]">
                Prepare interview questions and manage scheduled interviews for approved candidates.
              </p>
            </div>
            <Card flat className="justify-center text-center">
              <p className="text-sm text-[var(--text-soft)] italic">
                “Great hires start with great conversations.”
              </p>
              <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
            </Card>
          </div>

          {/* Summary cards */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Card>
              <StatCard label="Total Interviews" value={page.summary.total_interviews} />
            </Card>
            <Card>
              <StatCard label="Scheduled" value={page.summary.scheduled} accent />
            </Card>
            <Card>
              <StatCard label="Completed" value={page.summary.completed} />
            </Card>
            <Card>
              <StatCard label="Cancelled" value={page.summary.cancelled} />
            </Card>
          </div>

          {/* Scheduled Interviews */}
          <Card>
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3>Scheduled Interviews</h3>
                <p className="text-sm text-[var(--text-mute)]">
                  Track and manage interviews for approved candidates.
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search by candidate or role…"
                  className="min-w-[220px]"
                />
                <SimpleSelect
                  options={[
                    { value: "all", label: "All Jobs" },
                    ...page.filters.jobs.map((j) => ({ value: String(j.id), label: j.job_title })),
                  ]}
                  value={jobId}
                  onChange={(e) => setJobId(e.target.value)}
                  className="!w-auto"
                />
                <SimpleSelect
                  options={[
                    { value: "all", label: "All Status" },
                    ...page.filters.statuses.map((s) => ({ value: s, label: s })),
                  ]}
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="!w-auto"
                />
                <Button onClick={() => setScheduleOpen(true)}>+ Schedule Interview</Button>
              </div>
            </div>
            <DataTable
              columns={columns}
              rows={filteredInterviews.map((r) => ({ ...r, id: r.application_id }))}
              emptyText="No interviews scheduled yet. Approve a candidate, then schedule their interview here."
            />
          </Card>

          {/* Recent Activity */}
          <Card>
            <h3>Recent Activity</h3>
            <p className="text-sm text-[var(--text-mute)]">
              Track the latest interview-related updates.
            </p>
            {page.recent_activity.length === 0 ? (
              <p className="text-sm text-[var(--text-mute)]">No activity yet.</p>
            ) : (
              <ul className="flex flex-col gap-2">
                {page.recent_activity.map((item, idx) => (
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
        </>
      ) : null}

      <ScheduleInterviewModal
        key={String(scheduleOpen)}
        open={scheduleOpen}
        onOpenChange={setScheduleOpen}
        eligibleCandidates={page?.eligible_candidates ?? []}
        onScheduled={load}
      />

      <InterviewDetailModal
        applicationId={detailApplicationId}
        onOpenChange={(open) => !open && setDetailApplicationId(null)}
      />

      <OutcomeModal
        applicationId={outcomeApplicationId}
        onOpenChange={(open) => !open && setOutcomeApplicationId(null)}
        onRecorded={load}
      />
    </Shell>
  );
}

function ScheduleInterviewModal({
  open,
  onOpenChange,
  eligibleCandidates,
  onScheduled,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  eligibleCandidates: { application_id: number; candidate_name: string; job_role: string }[];
  onScheduled: () => void;
}) {
  const [applicationId, setApplicationId] = React.useState("");
  const [interviewType, setInterviewType] = React.useState("Technical");
  const [scheduledAt, setScheduledAt] = React.useState("");
  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const canSubmit = applicationId && interviewType && scheduledAt;

  async function handleSubmit() {
    if (!canSubmit) return;
    setSaving(true);
    setError(null);
    try {
      await scheduleInterview(
        Number(applicationId),
        interviewType,
        new Date(scheduledAt).toISOString(),
      );
      onScheduled();
      onOpenChange(false);
    } catch {
      setError("Could not schedule this interview. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Schedule Interview" closeOnOverlayClick>
      <div className="flex flex-col gap-4">
        <div>
          <label className="lm-label">Candidate</label>
          <SimpleSelect
            options={eligibleCandidates.map((c) => ({
              value: String(c.application_id),
              label: `${c.candidate_name} — ${c.job_role}`,
            }))}
            value={applicationId}
            onChange={(e) => setApplicationId(e.target.value)}
            placeholder="Select an approved candidate…"
          />
          {eligibleCandidates.length === 0 ? (
            <p className="mt-1 text-xs text-[var(--text-mute)]">
              No candidates are ready to schedule yet — approve a candidate and wait for interview
              questions to be generated first.
            </p>
          ) : null}
        </div>
        <div>
          <label className="lm-label">Interview Type</label>
          <SimpleSelect
            options={INTERVIEW_TYPES.map((t) => ({ value: t, label: t }))}
            value={interviewType}
            onChange={(e) => setInterviewType(e.target.value)}
          />
        </div>
        <div>
          <label className="lm-label">Date & Time</label>
          <Input
            type="datetime-local"
            value={scheduledAt}
            onChange={(e) => setScheduledAt(e.target.value)}
          />
        </div>
        {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
        <Button onClick={handleSubmit} disabled={!canSubmit || saving} className="self-end">
          {saving ? "Scheduling…" : "Schedule Interview"}
        </Button>
      </div>
    </Modal>
  );
}

function InterviewDetailModal({
  applicationId,
  onOpenChange,
}: {
  applicationId: number | null;
  onOpenChange: (open: boolean) => void;
}) {
  return (
    <Modal
      key={applicationId ?? "closed"}
      open={applicationId !== null}
      onOpenChange={onOpenChange}
      title="Interview Questions"
    >
      {applicationId !== null ? (
        <InterviewDetailBody key={applicationId} applicationId={applicationId} />
      ) : null}
    </Modal>
  );
}

function InterviewDetailBody({ applicationId }: { applicationId: number }) {
  const [detail, setDetail] = React.useState<InterviewDetail | null>(null);

  React.useEffect(() => {
    getInterviewDetail(applicationId).then(setDetail);
  }, [applicationId]);

  if (!detail) {
    return <LoadingState label="Loading questions…" />;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm font-semibold text-[var(--text)]">
        {detail.candidate_name} — {detail.job_role}
      </p>
      <div className="flex flex-wrap items-center gap-2 text-sm text-[var(--text-mute)]">
        <Badge variant="hold">{detail.ai_status_label}</Badge>
        <Badge variant={STATUS_BADGE[detail.status_label] ?? "neutral"}>
          {detail.status_label}
        </Badge>
        {detail.scheduled_at_display ? <span>{detail.scheduled_at_display}</span> : null}
        {detail.outcome_label ? (
          <Badge variant={detail.outcome === "hired" ? "ok" : "rejected"}>
            {detail.outcome_label}
          </Badge>
        ) : null}
      </div>
      {detail.outcome === "not_selected" && detail.outcome_reason ? (
        <p className="text-sm text-[var(--text-mute)]">
          Outcome reason: <span className="text-[var(--text-soft)]">{detail.outcome_reason}</span>
        </p>
      ) : null}

      <div>
        <h4 className="mb-2 text-sm font-semibold text-[var(--text)]">
          AI-Generated Interview Questions
        </h4>
        {detail.questions.length === 0 ? (
          <p className="text-sm text-[var(--text-mute)]">
            Questions have not been generated for this candidate yet.
          </p>
        ) : (
          <ul className="flex flex-col gap-3">
            {detail.questions.map((q, idx) => (
              <li key={idx} className="rounded-lg border border-[var(--border)] p-3">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium text-[var(--text)]">{q.question_text}</span>
                  {q.category ? <Badge variant="neutral">{q.category}</Badge> : null}
                </div>
                {q.evaluation_criteria ? (
                  <p className="mt-1 text-xs text-[var(--text-mute)]">
                    Evaluation criteria: {q.evaluation_criteria}
                  </p>
                ) : null}
              </li>
            ))}
          </ul>
        )}
      </div>

      {detail.invitation_subject ? (
        <div>
          <h4 className="mb-2 text-sm font-semibold text-[var(--text)]">Interview Invitation</h4>
          <div className="rounded-lg border border-[var(--border)] p-3 text-sm">
            <p className="font-medium text-[var(--text)]">{detail.invitation_subject}</p>
            <p className="mt-1 whitespace-pre-line text-[var(--text-soft)]">
              {detail.invitation_body}
            </p>
          </div>
        </div>
      ) : null}

      <div>
        <h4 className="mb-2 text-sm font-semibold text-[var(--text)]">Invitation Email</h4>
        <div className="flex flex-wrap items-center gap-2 text-sm text-[var(--text-mute)]">
          <Badge variant={EMAIL_STATUS_BADGE[detail.email_status] ?? "neutral"}>
            {detail.email_status_label}
          </Badge>
          {detail.recipient_email ? (
            <span>
              To: <span className="text-[var(--text-soft)]">{detail.recipient_email}</span>
              {detail.email_source ? ` (${EMAIL_SOURCE_LABEL[detail.email_source]})` : ""}
            </span>
          ) : (
            <span>No recipient email available</span>
          )}
          {detail.email_sent_at_display ? <span>{detail.email_sent_at_display}</span> : null}
        </div>
        {detail.email_status === "failed" && detail.email_error ? (
          <p className="mt-1 text-xs text-[var(--text-mute)]">{detail.email_error}</p>
        ) : null}
      </div>
    </div>
  );
}

function OutcomeModal({
  applicationId,
  onOpenChange,
  onRecorded,
}: {
  applicationId: number | null;
  onOpenChange: (open: boolean) => void;
  onRecorded: () => void;
}) {
  return (
    <Modal
      key={applicationId ?? "closed"}
      open={applicationId !== null}
      onOpenChange={onOpenChange}
      title="Record Recruitment Outcome"
    >
      {applicationId !== null ? (
        <OutcomeBody
          key={applicationId}
          applicationId={applicationId}
          onRecorded={() => {
            onRecorded();
            onOpenChange(false);
          }}
        />
      ) : null}
    </Modal>
  );
}

function OutcomeBody({
  applicationId,
  onRecorded,
}: {
  applicationId: number;
  onRecorded: () => void;
}) {
  const [detail, setDetail] = React.useState<InterviewDetail | null>(null);
  const [choice, setChoice] = React.useState<"hired" | "not_selected" | null>(null);
  const [reason, setReason] = React.useState("");
  const [saving, setSaving] = React.useState(false);

  React.useEffect(() => {
    getInterviewDetail(applicationId).then((d) => {
      setDetail(d);
      setReason(d.missing_skills[0] ? `Skill Gap: ${d.missing_skills[0]}` : "");
    });
  }, [applicationId]);

  async function handleSubmit() {
    if (!choice) return;
    if (choice === "not_selected" && !reason.trim()) return;
    setSaving(true);
    try {
      await setInterviewOutcome(
        applicationId,
        choice,
        choice === "not_selected" ? reason.trim() : undefined,
      );
      onRecorded();
    } finally {
      setSaving(false);
    }
  }

  if (!detail) {
    return <LoadingState label="Loading candidate…" />;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm text-[var(--text-mute)]">
        {detail.candidate_name} — {detail.job_role}. This outcome is final and feeds back into
        LOOP-MIND's closed-loop intelligence — a hire helps match future candidates for this role; a
        skill gap reason helps this candidate's preparation plan.
      </p>
      <div className="flex gap-2">
        <Button
          variant={choice === "hired" ? "primary" : "ghost"}
          onClick={() => setChoice("hired")}
        >
          Hired
        </Button>
        <Button
          variant={choice === "not_selected" ? "danger" : "ghost"}
          onClick={() => setChoice("not_selected")}
        >
          Not Selected
        </Button>
      </div>
      {choice === "not_selected" ? (
        <div>
          <label className="lm-label">Reason</label>
          <Textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="e.g. Skill Gap: System Design"
            rows={3}
          />
          <p className="mt-1 text-xs text-[var(--text-mute)]">
            This reason will be shown to the student so they can understand and improve. Be
            specific, especially for a skill gap.
          </p>
        </div>
      ) : null}
      <Button
        onClick={handleSubmit}
        disabled={!choice || (choice === "not_selected" && !reason.trim()) || saving}
        className="self-end"
      >
        {saving ? "Saving…" : "Confirm Outcome"}
      </Button>
    </div>
  );
}
