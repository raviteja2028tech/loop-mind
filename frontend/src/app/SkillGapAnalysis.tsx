import * as React from "react";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import { Search } from "lucide-react";
import { NavLink } from "react-router-dom";
import {
  Badge,
  type BadgeProps,
  Button,
  Card,
  ChartTooltip,
  ChartWell,
  ErrorState,
  GlobalFooter,
  Input,
  LoadingState,
  Modal,
  StudentNavbar,
  ReadinessRing,
  SearchableSelect,
  Shell,
  StatCard,
  Textarea,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import {
  ApiError,
  askWhatIf,
  createPreparationPlan,
  getRoleOptions,
  getSkillGapPage,
  putSkillGapTarget,
  type SkillGapPage,
  type SkillRow,
  type SkillStatus,
  type WhatIfAnswer,
} from "@/lib/api";

const DISTRIBUTION_COLORS = {
  already_strong: "var(--accent)",
  needs_improvement: "var(--warn)",
  missing: "var(--accent-deep)",
  not_relevant: "var(--border-hi)",
} as const;

const STATUS_BADGE: Record<SkillStatus, BadgeProps["variant"]> = {
  Strong: "ok",
  "To Improve": "hold",
  Missing: "rejected",
  "Not Relevant": "neutral",
  "Missing Evidence": "hold",
};

const PRIORITY_BADGE: Record<string, BadgeProps["variant"]> = {
  High: "rejected",
  Medium: "hold",
  Low: "neutral",
};

const FILTER_TABS: { key: "All" | SkillStatus; label: string }[] = [
  { key: "All", label: "All Skills" },
  { key: "To Improve", label: "To Improve" },
  { key: "Missing", label: "Missing" },
  { key: "Missing Evidence", label: "Missing Evidence" },
  { key: "Strong", label: "Strong" },
  { key: "Not Relevant", label: "Not Relevant" },
];

export default function SkillGapAnalysis() {
  const [page, setPage] = React.useState<SkillGapPage | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const load = React.useCallback(() => {
    getSkillGapPage()
      .then((data) => {
        setPage(data);
        setError(null);
      })
      .catch((err) => {
        setError(
          err instanceof ApiError ? "Could not load your skill gap analysis." : "Network error.",
        );
      });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  return (
    <Shell navbar={<StudentNavbar />} footer={<GlobalFooter />}>
      {!page && !error ? <LoadingState label="Loading your skill gap analysis…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {page ? <PageBody page={page} onRefresh={load} /> : null}
    </Shell>
  );
}

function PageBody({ page, onRefresh }: { page: SkillGapPage; onRefresh: () => void }) {
  const [activeTab, setActiveTab] = React.useState<"All" | SkillStatus>("All");
  const [search, setSearch] = React.useState("");
  const [whatIfOpen, setWhatIfOpen] = React.useState(false);
  const [resourceRow, setResourceRow] = React.useState<SkillRow | null>(null);

  const counts = React.useMemo(() => {
    const byStatus: Record<SkillStatus, number> = {
      Strong: 0,
      "To Improve": 0,
      Missing: 0,
      "Not Relevant": 0,
      "Missing Evidence": 0,
    };
    for (const row of page.skills) byStatus[row.status] += 1;
    return byStatus;
  }, [page.skills]);

  const visibleRows = React.useMemo(() => {
    return page.skills
      .filter((row) => activeTab === "All" || row.status === activeTab)
      .filter((row) => row.skill.toLowerCase().includes(search.trim().toLowerCase()));
  }, [page.skills, activeTab, search]);

  const distributionData = [
    { key: "already_strong", label: "Already Strong", value: page.distribution.already_strong },
    {
      key: "needs_improvement",
      label: "Needs Improvement",
      value: page.distribution.needs_improvement,
    },
    { key: "missing", label: "Missing", value: page.distribution.missing },
    { key: "not_relevant", label: "Not Relevant", value: page.distribution.not_relevant },
  ];
  const hasDistribution = distributionData.some((d) => d.value > 0);

  const columns: Column<SkillRow & { id: string }>[] = [
    { key: "skill", header: "Skill", render: (r) => r.skill },
    { key: "category", header: "Category", render: (r) => r.category },
    { key: "your_level", header: "Your Level", render: (r) => r.your_level },
    { key: "required_level", header: "Required Level", render: (r) => r.required_level },
    {
      key: "status",
      header: "Status",
      render: (r) => <Badge variant={STATUS_BADGE[r.status]}>{r.status}</Badge>,
    },
    {
      key: "priority",
      header: "Priority",
      render: (r) =>
        r.priority ? (
          <Badge variant={PRIORITY_BADGE[r.priority] ?? "neutral"}>{r.priority}</Badge>
        ) : (
          "—"
        ),
    },
    {
      key: "action",
      header: "Action",
      render: (r) =>
        r.resources ? (
          <Button variant="ghost" className="!px-2 !py-1 text-xs" onClick={() => setResourceRow(r)}>
            View Resources →
          </Button>
        ) : (
          "—"
        ),
    },
  ];

  return (
    <>
      {/* Header */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
        <div>
          <h2>Skill Gap Analysis</h2>
          <p className="mt-1 text-sm text-[var(--text-soft)]">
            Identify the most important skills to improve for your target roles.
          </p>
        </div>
        <Card flat className="justify-center text-center">
          <p className="text-sm text-[var(--text-soft)] italic">
            “A year from now, you’ll wish you had started today.”
          </p>
          <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
        </Card>
      </div>

      {/* First content row */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <TargetSelectionCard
          key={`${page.target_company ?? ""}-${page.target_role ?? ""}`}
          page={page}
          onRefresh={onRefresh}
        />

        <Card>
          <h3>Overall Readiness</h3>
          {page.readiness.has_analysis ? (
            <>
              <div className="flex items-center gap-4">
                <ReadinessRing percentage={page.readiness.readiness_percentage ?? 0} />
                <div>
                  <p className="font-medium text-[var(--text)]">{page.readiness.status_message}</p>
                </div>
              </div>
              {page.readiness.supporting_text ? (
                <p className="text-sm text-[var(--text-mute)]">{page.readiness.supporting_text}</p>
              ) : null}
            </>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">
              Select a target company to calculate your readiness.
            </p>
          )}
        </Card>

        <QuickActionsCard page={page} onWhatIf={() => setWhatIfOpen(true)} />
      </div>

      {/* Second content row */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card>
          <h3>Skill Gap Overview</h3>
          <p className="text-sm text-[var(--text-mute)]">
            Here's a summary of your skills for the selected role.
          </p>
          <div className="grid grid-cols-2 gap-3">
            <StatCard label="Total Required Skills" value={page.overview.total_required_skills} />
            <StatCard label="Skills You Have" value={page.overview.skills_you_have} accent />
            <StatCard label="Skills to Improve" value={page.overview.skills_to_improve} />
            <StatCard label="Missing Evidence" value={page.overview.missing_evidence} />
          </div>
        </Card>

        <Card>
          <h3>Skill Distribution</h3>
          {hasDistribution ? (
            <ChartWell>
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie
                    data={distributionData}
                    dataKey="value"
                    nameKey="label"
                    innerRadius={45}
                    outerRadius={70}
                  >
                    {distributionData.map((d) => (
                      <Cell
                        key={d.key}
                        fill={DISTRIBUTION_COLORS[d.key as keyof typeof DISTRIBUTION_COLORS]}
                      />
                    ))}
                  </Pie>
                  <ChartTooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartWell>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">No skill data to distribute yet.</p>
          )}
          <ul className="flex flex-col gap-1 text-xs text-[var(--text-mute)]">
            {distributionData.map((d) => (
              <li key={d.key} className="flex items-center gap-2">
                <span
                  className="inline-block size-2.5 rounded-full"
                  style={{
                    background: DISTRIBUTION_COLORS[d.key as keyof typeof DISTRIBUTION_COLORS],
                  }}
                />
                {d.label}: {d.value}
              </li>
            ))}
          </ul>
        </Card>

        <Card>
          <h3>Top Priority Areas</h3>
          <p className="text-sm text-[var(--text-mute)]">
            These skills will have the highest impact on your placement readiness.
          </p>
          {page.priority_areas.length === 0 ? (
            <p className="text-sm text-[var(--text-mute)]">No priority gaps identified yet.</p>
          ) : (
            <ol className="flex flex-col gap-2">
              {page.priority_areas.map((area) => (
                <li key={area.rank} className="flex items-center justify-between gap-3 text-sm">
                  <span className="text-[var(--text-soft)]">
                    {area.rank}. {area.skill}
                  </span>
                  <Badge variant={area.impact.startsWith("High") ? "rejected" : "hold"}>
                    {area.impact}
                  </Badge>
                </li>
              ))}
            </ol>
          )}
        </Card>
      </div>

      {/* Filters + search */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap gap-2">
          {FILTER_TABS.map((tab) => (
            <button
              key={tab.key}
              type="button"
              onClick={() => setActiveTab(tab.key)}
              className={"lm-nav-link" + (activeTab === tab.key ? " is-active" : "")}
            >
              {tab.label}
              {tab.key !== "All" ? ` (${counts[tab.key]})` : ""}
            </button>
          ))}
        </div>
        <div className="relative w-full max-w-[240px]">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-[var(--text-mute)]" />
          <Input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search skills…"
            className="pl-9"
          />
        </div>
      </div>

      {/* Skill Analysis Table */}
      <DataTable
        columns={columns}
        rows={visibleRows.map((r) => ({ ...r, id: r.skill }))}
        emptyText="No skills match this filter yet."
      />

      <WhatIfModal
        key={String(whatIfOpen)}
        open={whatIfOpen}
        onOpenChange={setWhatIfOpen}
        targetCompany={page.target_company}
        targetRole={page.target_role}
      />

      <Modal
        open={resourceRow !== null}
        onOpenChange={(open) => !open && setResourceRow(null)}
        title={resourceRow ? `Resources — ${resourceRow.skill}` : undefined}
      >
        <p className="text-sm text-[var(--text-soft)]">{resourceRow?.resources}</p>
      </Modal>
    </>
  );
}

function TargetSelectionCard({ page, onRefresh }: { page: SkillGapPage; onRefresh: () => void }) {
  const [company, setCompany] = React.useState<string | null>(page.target_company);
  const [role, setRole] = React.useState<string | null>(page.target_role);
  const [roleOptions, setRoleOptions] = React.useState<string[]>(page.role_options);
  const [saving, setSaving] = React.useState(false);

  function handleCompanyChange(value: string) {
    setCompany(value);
    setRole(null);
    getRoleOptions(value)
      .then(setRoleOptions)
      .catch(() => setRoleOptions([]));
  }

  async function handleSave() {
    if (!company) return;
    setSaving(true);
    try {
      await putSkillGapTarget(company, role);
      onRefresh();
    } finally {
      setSaving(false);
    }
  }

  const dirty = company !== page.target_company || role !== page.target_role;

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
      {dirty ? (
        <Button onClick={handleSave} disabled={!company || saving} className="self-start">
          {saving ? "Saving…" : "Update"}
        </Button>
      ) : null}
    </Card>
  );
}

function QuickActionsCard({ page, onWhatIf }: { page: SkillGapPage; onWhatIf: () => void }) {
  const [planStatus, setPlanStatus] = React.useState<string | null>(null);
  const [planGenerated, setPlanGenerated] = React.useState(false);
  const [generating, setGenerating] = React.useState(false);
  const hasTarget = page.target_company !== null;

  async function handleGeneratePlan() {
    if (!page.target_company) return;
    setGenerating(true);
    setPlanStatus(null);
    setPlanGenerated(false);
    try {
      const result = await createPreparationPlan(page.target_company, page.target_role);
      setPlanStatus(`Personalized plan generated and saved (version ${result.version}).`);
      setPlanGenerated(true);
    } catch {
      setPlanStatus("Could not generate a plan. Please try again.");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <Card>
      <h3>Quick Actions</h3>
      <Button
        onClick={handleGeneratePlan}
        disabled={!hasTarget || generating}
        className="self-start"
      >
        {generating ? "Generating…" : "Get Personalized Plan →"}
      </Button>
      <Button variant="ghost" onClick={onWhatIf} disabled={!hasTarget} className="self-start">
        Try What-If Analysis →
      </Button>
      {planStatus ? <p className="text-xs text-[var(--text-mute)]">{planStatus}</p> : null}
      {planGenerated ? (
        <NavLink to="/app/preparation-plan" className="lm-nav-link self-start !px-0 text-xs">
          View your plan on the Preparation Plan page →
        </NavLink>
      ) : null}
      {!hasTarget ? (
        <p className="text-xs text-[var(--text-mute)]">Select a target company first.</p>
      ) : null}
    </Card>
  );
}

function WhatIfModal({
  open,
  onOpenChange,
  targetCompany,
  targetRole,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  targetCompany: string | null;
  targetRole: string | null;
}) {
  const [question, setQuestion] = React.useState("");
  const [result, setResult] = React.useState<WhatIfAnswer | null>(null);
  const [asking, setAsking] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function handleAnalyze() {
    if (!targetCompany || !question.trim()) return;
    setAsking(true);
    setError(null);
    // Skill Gap What-If Analysis SDD §17: never leave the previous
    // answer on screen while a new one is being generated — that would
    // read as stale analysis presented as if it were the fresh result.
    setResult(null);
    try {
      const response = await askWhatIf(targetCompany, targetRole, question.trim());
      setResult(response.result);
    } catch {
      setError("Could not analyze that question. Please try again.");
    } finally {
      setAsking(false);
    }
  }

  // Skill Gap What-If Analysis SDD §10-13: an explicit Reset, distinct
  // from closing the modal — clears only this temporary simulation state
  // (never calls any API, never touches the student's actual data) so the
  // student can try a different hypothetical without losing their place.
  function handleReset() {
    setQuestion("");
    setResult(null);
    setError(null);
  }

  const improvement =
    result?.current_readiness_percentage != null && result?.projected_readiness_percentage != null
      ? result.projected_readiness_percentage - result.current_readiness_percentage
      : null;

  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Try What-If Analysis">
      <div className="flex flex-col gap-4">
        <p className="text-sm text-[var(--text-mute)]">What if I learn Generative AI?</p>
        <Textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What if I learn Generative AI?"
          rows={3}
        />
        {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
        {result ? (
          <Card flat className="flex flex-col gap-3">
            <p className="text-sm text-[var(--text-soft)]">{result.answer}</p>

            {result.current_readiness_percentage !== null &&
            result.projected_readiness_percentage !== null ? (
              <div className="flex flex-wrap items-center gap-8">
                <div>
                  <p className="text-xs text-[var(--text-mute)]">Current Readiness</p>
                  <p className="text-lg font-semibold text-[var(--text)]">
                    {result.current_readiness_percentage}%
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-mute)]">Projected Readiness</p>
                  <p className="text-lg font-semibold text-[var(--accent)]">
                    {result.projected_readiness_percentage}%
                  </p>
                </div>
                {improvement !== null ? (
                  <div>
                    <p className="text-xs text-[var(--text-mute)]">Potential Improvement</p>
                    <p className="text-lg font-semibold text-[var(--accent)]">
                      {improvement > 0 ? "+" : ""}
                      {improvement}%
                    </p>
                  </div>
                ) : null}
              </div>
            ) : null}

            {result.relevant_roles.length > 0 ? (
              <div>
                <h4 className="text-sm font-semibold text-[var(--text)]">
                  Relevant Roles at {targetCompany}
                </h4>
                <ul className="mt-1 flex flex-wrap gap-2">
                  {result.relevant_roles.map((role) => (
                    <li
                      key={role}
                      className="rounded-full border border-[var(--border)] px-3 py-1 text-xs text-[var(--text-soft)]"
                    >
                      {role}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </Card>
        ) : null}
        <div className="flex justify-center gap-3">
          <Button onClick={handleAnalyze} disabled={!question.trim() || asking}>
            {asking ? "Analyzing…" : "Generate"}
          </Button>
          {result || question || error ? (
            <Button variant="ghost" onClick={handleReset} disabled={asking}>
              Reset
            </Button>
          ) : null}
        </div>
      </div>
    </Modal>
  );
}
