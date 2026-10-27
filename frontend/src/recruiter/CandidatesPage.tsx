import * as React from "react";
import ReactFlow, { Background, Controls, type Edge, type Node } from "reactflow";
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
  flowNodeTypes,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import {
  ApiError,
  approveCandidate,
  disapproveCandidate,
  getCandidatesPage,
  getCandidateWorkflow,
  type CandidateFilters,
  type CandidateRow,
  type CandidatesPageData,
  type CandidateWorkflow,
} from "@/lib/api";
import { RecruiterFooter } from "@/recruiter/RecruiterFooter";

const STATUS_BADGE: Record<string, "ok" | "hold" | "rejected" | "neutral"> = {
  Shortlisted: "ok",
  "Under Review": "hold",
  Hold: "hold",
  Rejected: "rejected",
};

export default function CandidatesPage() {
  const [page, setPage] = React.useState<CandidatesPageData | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [search, setSearch] = React.useState("");
  const [jobId, setJobId] = React.useState("all");
  const [status, setStatus] = React.useState("all");
  const [aiEvaluation, setAiEvaluation] = React.useState("all");
  const [selected, setSelected] = React.useState<CandidateRow | null>(null);

  const load = React.useCallback(() => {
    const filters: CandidateFilters = { search: search || undefined };
    if (jobId !== "all") filters.job_id = Number(jobId);
    if (status !== "all") filters.status = status;
    if (aiEvaluation !== "all") filters.ai_evaluation = aiEvaluation;
    getCandidatesPage(filters)
      .then((data) => {
        setPage(data);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load candidates." : "Network error.");
      });
  }, [search, jobId, status, aiEvaluation]);

  React.useEffect(() => {
    load();
  }, [load]);

  const columns: Column<CandidateRow & { id: number }>[] = [
    { key: "candidate_name", header: "Candidate Name", render: (r) => r.candidate_name },
    { key: "applied_role", header: "Applied Role", render: (r) => r.applied_role },
    { key: "applied_on", header: "Applied On", render: (r) => r.applied_relative },
    {
      key: "ai_score",
      header: "AI Score",
      render: (r) => (r.ai_score !== null ? `${r.ai_score}/100` : "—"),
    },
    {
      key: "matching_factors",
      header: "Matching Factors",
      render: (r) => r.matching_factors ?? "—",
    },
    {
      key: "status",
      header: "Status",
      render: (r) => (
        <Badge variant={STATUS_BADGE[r.status_label] ?? "neutral"}>{r.status_label}</Badge>
      ),
    },
    {
      key: "action",
      header: "Action",
      render: (r) => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" className="!px-2 !py-1 text-xs" onClick={() => setSelected(r)}>
            View Evaluation →
          </Button>
          <Button variant="ghost" disabled className="!px-2 !py-1 text-xs">
            ⋮
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Shell
      navbar={<RecruiterNavbar />}
      footer={<RecruiterFooter />}
    >
      {!page && !error ? <LoadingState label="Loading candidates…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {page ? (
        <>
          {/* Header */}
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
            <div>
              <h2>Candidates</h2>
              <p className="mt-1 text-sm text-[var(--text-soft)]">
                Review candidates, AI evaluations, and recruitment progress.
              </p>
            </div>
            <Card flat className="justify-center text-center">
              <p className="text-sm text-[var(--text-soft)] italic">
                “Great candidates build greater companies.”
              </p>
              <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
            </Card>
          </div>

          {/* Summary cards — Recruiter Dashboard — Final Specification: no
             separate Pending Approval card here either. */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Card>
              <StatCard label="Total Candidates" value={page.summary.total_candidates} />
            </Card>
            <Card>
              <StatCard label="Shortlisted" value={page.summary.shortlisted} accent />
            </Card>
            <Card>
              <StatCard label="Under Review" value={page.summary.under_review} />
            </Card>
            <Card>
              <StatCard label="Rejected" value={page.summary.rejected} />
            </Card>
          </div>

          {/* All Candidates */}
          <Card>
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3>All Candidates</h3>
                <p className="text-sm text-[var(--text-mute)]">
                  View and manage candidates across your job postings.
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search candidates by name, role, or skills…"
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
                <SimpleSelect
                  options={[
                    { value: "all", label: "All AI Evaluation" },
                    ...page.filters.ai_evaluations.map((s) => ({ value: s, label: s })),
                  ]}
                  value={aiEvaluation}
                  onChange={(e) => setAiEvaluation(e.target.value)}
                  className="!w-auto"
                />
                <Button variant="ghost" onClick={load}>
                  Refresh
                </Button>
              </div>
            </div>
            <DataTable
              columns={columns}
              rows={page.candidates.map((c) => ({ ...c, id: c.application_id }))}
              emptyText="No candidates match your search and filters yet."
            />
          </Card>

          {/* AI Recruitment Workflow */}
          <Card>
            <h3>AI Recruitment Workflow</h3>
            <p className="text-sm text-[var(--text-mute)]">
              End-to-end process for each candidate.
            </p>
            {selected ? (
              <WorkflowPanel key={selected.application_id} selected={selected} onDecided={load} />
            ) : (
              <p className="text-sm text-[var(--text-mute)]">
                Click "View Evaluation →" on a candidate to see their recruitment workflow here.
              </p>
            )}
          </Card>
        </>
      ) : null}
    </Shell>
  );
}

function WorkflowPanel({ selected, onDecided }: { selected: CandidateRow; onDecided: () => void }) {
  const [workflow, setWorkflow] = React.useState<CandidateWorkflow | null>(null);
  const [disapproveOpen, setDisapproveOpen] = React.useState(false);
  const [deciding, setDeciding] = React.useState(false);

  React.useEffect(() => {
    getCandidateWorkflow(selected.application_id).then(setWorkflow);
  }, [selected]);

  async function handleApprove() {
    setDeciding(true);
    try {
      const updated = await approveCandidate(selected.application_id);
      setWorkflow(updated);
      onDecided();
    } finally {
      setDeciding(false);
    }
  }

  async function handleDisapproved(updated: CandidateWorkflow) {
    setWorkflow(updated);
    onDecided();
  }

  if (!workflow) {
    return <LoadingState label="Loading workflow…" />;
  }

  const nodes: Node[] = workflow.stages.map((stage, idx) => ({
    id: stage.key,
    type: "workflow",
    position: { x: idx * 190, y: 0 },
    data: { label: stage.label, state: stage.state },
    draggable: false,
  }));
  const edges: Edge[] = workflow.stages.slice(1).map((stage, idx) => {
    const previous = workflow.stages[idx];
    const isActive = previous.state === "completed" || previous.state === "approved";
    return {
      id: `${previous.key}-${stage.key}`,
      source: previous.key,
      target: stage.key,
      animated: isActive,
    };
  });

  return (
    <div className="flex flex-col gap-4">
      <Card flat>
        <p className="text-xs font-medium text-[var(--text-mute)]">Selected Candidate</p>
        <p className="text-lg font-semibold text-[var(--text)]">
          {workflow.selected_candidate.candidate_name}
        </p>
        <p className="text-sm text-[var(--text-soft)]">
          {workflow.selected_candidate.applied_role}
        </p>
        <p className="text-sm text-[var(--text-mute)]">
          AI Score:{" "}
          <span className="font-semibold text-[var(--accent)]">
            {workflow.selected_candidate.ai_score ?? "—"}/100
          </span>
        </p>
        {workflow.matched_skills.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {workflow.matched_skills.map((skill) => (
              <Badge key={skill} variant="ok">
                {skill}
              </Badge>
            ))}
            {workflow.missing_skills.map((skill) => (
              <Badge key={skill} variant="rejected">
                {skill}
              </Badge>
            ))}
          </div>
        ) : null}

        {/* Historical Intelligence — phase.md Phase 16: a real signal from
            this recruiter's own previously-hired candidates for this role. */}
        {workflow.historical_signal ? (
          <p className="text-xs text-[var(--text-mute)]">
            📈 Historical signal: {workflow.historical_signal}
          </p>
        ) : null}

        {/* Human Approval — phase.md Phase 14 */}
        <div className="flex flex-wrap items-center gap-3 border-t border-[var(--border)] pt-3">
          {workflow.human_decision === "approved" ? (
            <Badge variant="ok">Approved</Badge>
          ) : workflow.human_decision === "disapproved" ? (
            <div className="flex flex-col gap-1">
              <Badge variant="rejected">Disapproved</Badge>
              {workflow.disapproval_reason ? (
                <span className="text-xs text-[var(--text-mute)]">
                  Reason: {workflow.disapproval_reason}
                </span>
              ) : null}
            </div>
          ) : null}
          <Button onClick={handleApprove} disabled={deciding}>
            Approve
          </Button>
          <Button variant="danger" onClick={() => setDisapproveOpen(true)} disabled={deciding}>
            Disapprove
          </Button>
        </div>
      </Card>

      <DisapproveModal
        open={disapproveOpen}
        onOpenChange={setDisapproveOpen}
        applicationId={selected.application_id}
        suggestedSkill={workflow.missing_skills[0]}
        onDisapproved={handleDisapproved}
      />

      <div style={{ height: 160 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={flowNodeTypes}
          fitView
          nodesConnectable={false}
          elementsSelectable={false}
          proOptions={{ hideAttribution: true }}
        >
          <Background />
          <Controls showInteractive={false} />
        </ReactFlow>
      </div>

      {/* Recruiter Interview Invitation & Demo Email Specification §10: the
          actual generated interview/email result, not just a tick on the
          diagram above. */}
      {workflow.interview_question_count > 0 || workflow.email_status ? (
        <Card flat>
          <p className="text-xs font-medium text-[var(--text-mute)]">Interview &amp; Email</p>
          <div className="flex flex-wrap items-center gap-2 text-sm text-[var(--text-mute)]">
            {workflow.interview_question_count > 0 ? (
              <span>{workflow.interview_question_count} interview questions prepared</span>
            ) : null}
            {workflow.email_status_label ? (
              <Badge
                variant={
                  workflow.email_status === "sent"
                    ? "ok"
                    : workflow.email_status === "failed"
                      ? "rejected"
                      : workflow.email_status === "sending"
                        ? "hold"
                        : "neutral"
                }
              >
                Email: {workflow.email_status_label}
              </Badge>
            ) : null}
            {workflow.recipient_email ? <span>To: {workflow.recipient_email}</span> : null}
          </div>
          {workflow.email_status === "failed" && workflow.email_error ? (
            <p className="text-xs text-[var(--text-mute)]">{workflow.email_error}</p>
          ) : null}
        </Card>
      ) : null}
    </div>
  );
}

function DisapproveModal({
  open,
  onOpenChange,
  applicationId,
  suggestedSkill,
  onDisapproved,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  applicationId: number;
  suggestedSkill: string | undefined;
  onDisapproved: (workflow: CandidateWorkflow) => void;
}) {
  const [reason, setReason] = React.useState(suggestedSkill ? `Skill Gap: ${suggestedSkill}` : "");
  const [saving, setSaving] = React.useState(false);

  async function handleSubmit() {
    if (!reason.trim()) return;
    setSaving(true);
    try {
      const updated = await disapproveCandidate(applicationId, reason.trim());
      onDisapproved(updated);
      onOpenChange(false);
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal key={String(open)} open={open} onOpenChange={onOpenChange} title="Disapprove Candidate">
      <div className="flex flex-col gap-4">
        <p className="text-sm text-[var(--text-mute)]">
          This reason will be shown to the student so they can understand and improve. Be specific,
          especially for a skill gap.
        </p>
        <Textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="e.g. Skill Gap: System Design"
          rows={3}
        />
        <Button variant="danger" onClick={handleSubmit} disabled={!reason.trim() || saving}>
          {saving ? "Saving…" : "Confirm Disapproval"}
        </Button>
      </div>
    </Modal>
  );
}
