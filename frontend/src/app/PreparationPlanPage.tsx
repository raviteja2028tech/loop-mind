import * as React from "react";
import {
  Badge,
  Button,
  Card,
  ErrorState,
  GlobalFooter,
  Input,
  LoadingState,
  Modal,
  StudentNavbar,
  ReadinessRing,
  SearchableSelect,
  Shell,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import {
  ApiError,
  addPreparationGoal,
  generatePreparationPlanPage,
  getRoleOptions,
  getPreparationPlanPage,
  togglePreparationGoal,
  type GoalKind,
  type PlanRow,
  type PreparationPlanPageData,
} from "@/lib/api";

const FILTER_TABS = [
  "All",
  "DSA",
  "Development",
  "System Design",
  "Databases",
  "Interview Prep",
  "Projects",
  "Other",
];

const PRIORITY_BADGE: Record<string, "rejected" | "hold" | "neutral"> = {
  High: "rejected",
  Medium: "hold",
  Low: "neutral",
};

export default function PreparationPlanPage() {
  const [page, setPage] = React.useState<PreparationPlanPageData | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const load = React.useCallback(() => {
    getPreparationPlanPage()
      .then((data) => {
        setPage(data);
        setError(null);
      })
      .catch((err) => {
        setError(
          err instanceof ApiError ? "Could not load your preparation plan." : "Network error.",
        );
      });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  return (
    <Shell navbar={<StudentNavbar />} footer={<GlobalFooter />}>
      {!page && !error ? <LoadingState label="Loading your preparation plan…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {page ? <PageBody page={page} onRefresh={load} /> : null}
    </Shell>
  );
}

function PageBody({ page, onRefresh }: { page: PreparationPlanPageData; onRefresh: () => void }) {
  const [activeFilter, setActiveFilter] = React.useState("All");
  const [viewRow, setViewRow] = React.useState<PlanRow | null>(null);

  const visibleRows = page.plan_items.filter(
    (row) => activeFilter === "All" || row.filter_category === activeFilter,
  );

  const columns: Column<PlanRow & { id: string }>[] = [
    { key: "skill", header: "Skill / Topic", render: (r) => r.skill },
    { key: "category", header: "Category", render: (r) => r.category },
    { key: "current_level", header: "Current Level", render: (r) => r.current_level },
    { key: "target_level", header: "Target Level", render: (r) => r.target_level },
    { key: "start_date", header: "Start Date", render: (r) => r.start_date },
    { key: "end_date", header: "End Date", render: (r) => r.end_date },
    { key: "status", header: "Status", render: (r) => <Badge variant="hold">{r.status}</Badge> },
    {
      key: "priority",
      header: "Priority",
      render: (r) => <Badge variant={PRIORITY_BADGE[r.priority] ?? "neutral"}>{r.priority}</Badge>,
    },
    { key: "resources", header: "Resources", render: (r) => r.resources.slice(0, 40) + "…" },
    {
      key: "action",
      header: "Action",
      render: (r) => (
        <Button variant="ghost" className="!px-2 !py-1 text-xs" onClick={() => setViewRow(r)}>
          View Plan →
        </Button>
      ),
    },
  ];

  function handleExport() {
    const blob = new Blob([JSON.stringify(page, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `preparation-plan-${page.target_company ?? "plan"}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <>
      {/* Header */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
        <div>
          <h2>Preparation Plan</h2>
          <p className="mt-1 text-sm text-[var(--text-soft)]">
            A personalized plan based on your current year, goals and target company.
          </p>
        </div>
        <Card flat className="justify-center text-center">
          <p className="text-sm text-[var(--text-soft)] italic">
            “A year from now, you’ll wish you had started today.”
          </p>
          <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
        </Card>
      </div>

      {/* Configuration + Readiness */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1.4fr_1fr]">
        <ConfigurationCard page={page} onGenerated={onRefresh} />

        <Card>
          <h3>Current Readiness</h3>
          {page.readiness.has_analysis ? (
            <div className="flex items-center gap-4">
              <ReadinessRing percentage={page.readiness.readiness_percentage ?? 0} />
              <p className="font-medium text-[var(--text)]">{page.readiness.status_message}</p>
            </div>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">
              Select a target company and run a Skill Gap Analysis to see your readiness here.
            </p>
          )}
        </Card>
      </div>

      {/* Year-Wise Focus + Goals/Recommendations */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <h3>Year-Wise Focus</h3>
          <div className="flex items-center">
            {page.year_wise_focus.map((y, idx) => (
              <React.Fragment key={y.year}>
                {idx > 0 ? (
                  <div className="mx-1 h-px flex-1" style={{ background: "var(--border)" }} />
                ) : null}
                <span
                  className="whitespace-nowrap rounded-full px-3 py-1.5 text-xs font-medium"
                  style={{
                    background: y.is_current ? "var(--accent)" : "var(--raised)",
                    color: y.is_current ? "var(--bg)" : "var(--text-mute)",
                  }}
                >
                  {y.year}
                </span>
              </React.Fragment>
            ))}
          </div>
          <p className="text-sm text-[var(--text-mute)]">
            {page.year_wise_focus.find((y) => y.is_current)?.focus_text ??
              "Set your academic year to see your focus for this stage."}
          </p>

          {page.has_plan && page.plan_items.length > 0 ? (
            <div className="mt-2 flex flex-col gap-3">
              {page.plan_items.map((item, idx) => (
                <div key={item.skill} className="flex gap-3">
                  <div className="flex flex-col items-center">
                    <div
                      className="flex size-7 shrink-0 items-center justify-center rounded-full text-xs font-semibold"
                      style={{ background: "var(--accent)", color: "var(--bg)" }}
                    >
                      {idx + 1}
                    </div>
                    {idx < page.plan_items.length - 1 ? (
                      <div className="my-0.5 w-px flex-1" style={{ background: "var(--border)" }} />
                    ) : null}
                  </div>
                  <div className="pb-2">
                    <p className="text-sm font-medium text-[var(--text)]">{item.skill}</p>
                    <p className="text-xs text-[var(--text-mute)]">
                      {item.start_date} → {item.end_date}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : null}
        </Card>

        <div className="flex flex-col gap-4">
          <GoalsCard page={page} onRefresh={onRefresh} />
          <Card>
            <h3>AI Recommendations</h3>
            <ol className="flex flex-col gap-2">
              {page.recommendations.map((rec, idx) => (
                <li key={idx} className="text-sm text-[var(--text-soft)]">
                  {rec.title} →
                </li>
              ))}
            </ol>
          </Card>
        </div>
      </div>

      {/* Detailed Preparation Plan */}
      <Card>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h3>Detailed Preparation Plan</h3>
            <p className="text-sm text-[var(--text-mute)]">
              A step-by-step plan to help you achieve your goals.
            </p>
          </div>
          <Button variant="ghost" onClick={handleExport} disabled={!page.has_plan}>
            Export Plan ↓
          </Button>
        </div>

        <div className="flex flex-wrap gap-2">
          {FILTER_TABS.map((tab) => (
            <button
              key={tab}
              type="button"
              onClick={() => setActiveFilter(tab)}
              className={"lm-nav-link" + (activeFilter === tab ? " is-active" : "")}
            >
              {tab}
            </button>
          ))}
        </div>

        <DataTable
          columns={columns}
          rows={visibleRows.map((r) => ({ ...r, id: r.skill }))}
          emptyText={
            page.has_plan
              ? "No plan items match this filter yet."
              : "Generate a preparation plan above to see your step-by-step plan here."
          }
        />
      </Card>

      <Modal
        open={viewRow !== null}
        onOpenChange={(open) => !open && setViewRow(null)}
        title={viewRow ? `Plan Details — ${viewRow.skill}` : undefined}
      >
        {viewRow ? (
          <div className="flex flex-col gap-2 text-sm text-[var(--text-soft)]">
            <p>
              <strong>Category:</strong> {viewRow.category}
            </p>
            <p>
              <strong>Current → Target Level:</strong> {viewRow.current_level} →{" "}
              {viewRow.target_level}
            </p>
            <p>
              <strong>Timeline:</strong> {viewRow.start_date} to {viewRow.end_date}
            </p>
            <p>
              <strong>Status:</strong> {viewRow.status} &nbsp; <strong>Priority:</strong>{" "}
              {viewRow.priority}
            </p>
            <p>{viewRow.resources}</p>
          </div>
        ) : null}
      </Modal>
    </>
  );
}

function ConfigurationCard({
  page,
  onGenerated,
}: {
  page: PreparationPlanPageData;
  onGenerated: () => void;
}) {
  const [company, setCompany] = React.useState<string | null>(page.target_company);
  const [role, setRole] = React.useState<string | null>(page.target_role);
  const [academicYear, setAcademicYear] = React.useState<string | null>(page.academic_year);
  const [roleOptions, setRoleOptions] = React.useState<string[]>(page.role_options);
  const [generating, setGenerating] = React.useState(false);

  function handleCompanyChange(value: string) {
    setCompany(value);
    setRole(null);
    getRoleOptions(value)
      .then(setRoleOptions)
      .catch(() => setRoleOptions([]));
  }

  async function handleGenerate() {
    if (!company) return;
    setGenerating(true);
    try {
      await generatePreparationPlanPage(company, role, academicYear);
      onGenerated();
    } finally {
      setGenerating(false);
    }
  }

  return (
    <Card>
      <h3>Select Target Company</h3>
      <SearchableSelect
        options={page.company_options.map((name) => ({ value: name, label: name }))}
        value={company}
        onChange={handleCompanyChange}
        placeholder="Select a company…"
        searchPlaceholder="Search companies…"
      />
      <h3>Select Target Role</h3>
      <SearchableSelect
        options={roleOptions.map((name) => ({ value: name, label: name }))}
        value={role}
        onChange={setRole}
        placeholder="Select a role…"
        searchPlaceholder="Search roles…"
        disabled={!company}
      />
      <h3>Your Academic Year</h3>
      <SearchableSelect
        options={page.academic_year_options.map((y) => ({ value: y, label: y }))}
        value={academicYear}
        onChange={setAcademicYear}
        placeholder="Select academic year…"
      />
      <Button onClick={handleGenerate} disabled={!company || generating} className="self-center">
        {generating ? "Generating…" : "Generate Preparation Plan →"}
      </Button>
    </Card>
  );
}

function GoalsCard({ page, onRefresh }: { page: PreparationPlanPageData; onRefresh: () => void }) {
  async function handleToggle(kind: GoalKind, goalId: string) {
    await togglePreparationGoal(kind, goalId);
    onRefresh();
  }

  return (
    <Card>
      <h3>Your Goals</h3>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <GoalColumn
          label="Short-Term Goals"
          kind="short_term"
          goals={page.short_term_goals}
          onToggle={handleToggle}
          onAdded={onRefresh}
        />
        <GoalColumn
          label="Long-Term Goals"
          kind="long_term"
          goals={page.long_term_goals}
          onToggle={handleToggle}
          onAdded={onRefresh}
        />
      </div>
    </Card>
  );
}

function GoalColumn({
  label,
  kind,
  goals,
  onToggle,
  onAdded,
}: {
  label: string;
  kind: GoalKind;
  goals: PreparationPlanPageData["short_term_goals"];
  onToggle: (kind: GoalKind, goalId: string) => void;
  onAdded: () => void;
}) {
  const [text, setText] = React.useState("");
  const [adding, setAdding] = React.useState(false);

  async function handleAdd() {
    if (!text.trim()) return;
    setAdding(true);
    try {
      await addPreparationGoal(kind, text.trim());
      setText("");
      onAdded();
    } finally {
      setAdding(false);
    }
  }

  return (
    <div className="flex flex-col gap-2">
      <span className="text-xs font-medium text-[var(--text-mute)]">{label}</span>
      {goals.length === 0 ? (
        <p className="text-xs text-[var(--text-mute)]">No goals yet.</p>
      ) : (
        <ul className="flex flex-col gap-1.5">
          {goals.map((g) => (
            <li key={g.id} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={g.completed}
                onChange={() => onToggle(kind, g.id)}
                className="size-3.5"
              />
              <span
                className={
                  g.completed ? "text-[var(--text-mute)] line-through" : "text-[var(--text-soft)]"
                }
              >
                {g.text}
              </span>
            </li>
          ))}
        </ul>
      )}
      <div className="flex gap-2">
        <Input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add a goal…"
          className="text-xs"
        />
        <Button
          variant="ghost"
          onClick={handleAdd}
          disabled={!text.trim() || adding}
          className="!px-2 !py-1 text-xs"
        >
          Add
        </Button>
      </div>
    </div>
  );
}
