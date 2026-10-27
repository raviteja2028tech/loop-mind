import * as React from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import {
  Card,
  ChartTooltip,
  ChartWell,
  ErrorState,
  LoadingState,
  RecruiterNavbar,
  Shell,
  StatCard,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import {
  ApiError,
  getRecruiterAnalytics,
  type CompanyPattern,
  type RecruiterAnalyticsData,
} from "@/lib/api";
import { RecruiterFooter } from "@/recruiter/RecruiterFooter";

const OUTCOME_COLORS: Record<string, string> = {
  Hired: "var(--accent)",
  "Shortlisted (Pending)": "var(--accent-soft)",
  "Under Review": "var(--warn)",
  "Not Selected": "var(--danger)",
  Disapproved: "var(--accent-deep)",
};

export default function AnalyticsPage() {
  const [data, setData] = React.useState<RecruiterAnalyticsData | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getRecruiterAnalytics()
      .then((d) => {
        setData(d);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load analytics." : "Network error.");
      });
  }, []);

  return (
    <Shell
      navbar={<RecruiterNavbar />}
      footer={<RecruiterFooter />}
    >
      {!data && !error ? <LoadingState label="Loading analytics…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {data ? <AnalyticsBody data={data} /> : null}
    </Shell>
  );
}

function AnalyticsBody({ data }: { data: RecruiterAnalyticsData }) {
  const companyColumns: Column<CompanyPattern & { id: number }>[] = [
    { key: "job_title", header: "Job Title", render: (r) => r.job_title },
    { key: "job_role", header: "Role Type", render: (r) => r.job_role },
    { key: "applications", header: "Applications", render: (r) => r.applications },
    { key: "hire_rate", header: "Hire Rate", render: (r) => `${r.hire_rate_percentage}%` },
    {
      key: "avg_score",
      header: "Avg. AI Score",
      render: (r) => (r.average_ai_score !== null ? `${r.average_ai_score}/100` : "—"),
    },
  ];

  const hasOutcomes = data.outcomes.length > 0;
  const profile = data.successful_candidate_profile;

  return (
    <>
      {/* Header */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
        <div>
          <h2>Recruitment Analytics</h2>
          <p className="mt-1 text-sm text-[var(--text-soft)]">
            Historical intelligence across your jobs, candidates, and recruitment outcomes.
          </p>
        </div>
        <Card flat className="justify-center text-center">
          <p className="text-sm text-[var(--text-soft)] italic">
            “What gets measured gets improved.”
          </p>
          <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
        </Card>
      </div>

      {/* Recruitment funnel */}
      <Card>
        <h3>Recruitment Funnel</h3>
        <p className="text-sm text-[var(--text-mute)]">
          Applications moving through each stage of your recruitment process.
        </p>
        <ChartWell>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data.funnel}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="label" tickLine={false} axisLine={false} />
              <YAxis allowDecimals={false} tickLine={false} axisLine={false} width={28} />
              <ChartTooltip />
              <Bar dataKey="count" fill="var(--accent)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartWell>
      </Card>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Candidate outcomes */}
        <Card>
          <h3>Candidate Outcomes</h3>
          <p className="text-sm text-[var(--text-mute)]">
            Where every candidate ended up across your job postings.
          </p>
          {hasOutcomes ? (
            <>
              <ChartWell>
                <ResponsiveContainer width="100%" height={180}>
                  <PieChart>
                    <Pie
                      data={data.outcomes}
                      dataKey="count"
                      nameKey="label"
                      innerRadius={45}
                      outerRadius={70}
                    >
                      {data.outcomes.map((slice) => (
                        <Cell
                          key={slice.label}
                          fill={OUTCOME_COLORS[slice.label] ?? "var(--accent)"}
                        />
                      ))}
                    </Pie>
                    <ChartTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </ChartWell>
              <ul className="flex flex-col gap-1 text-xs text-[var(--text-mute)]">
                {data.outcomes.map((slice) => (
                  <li key={slice.label} className="flex items-center gap-2">
                    <span
                      className="inline-block size-2.5 rounded-full"
                      style={{ background: OUTCOME_COLORS[slice.label] ?? "var(--accent)" }}
                    />
                    {slice.label}: {slice.count}
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">No candidates yet.</p>
          )}
        </Card>

        {/* Successful-candidate characteristics */}
        <Card>
          <h3>Successful-Candidate Characteristics</h3>
          <p className="text-sm text-[var(--text-mute)]">
            A profile built from your own previously-hired candidates.
          </p>
          <div className="grid grid-cols-2 gap-3">
            <StatCard label="Total Hired" value={profile.total_hired} accent />
            <StatCard label="Avg. AI Score" value={profile.average_ai_score ?? 0} />
          </div>
          {profile.top_skills.length > 0 ? (
            <div>
              <p className="mb-2 text-xs font-medium text-[var(--text-mute)]">
                Most common skills among hires
              </p>
              <div className="flex flex-wrap gap-2">
                {profile.top_skills.map((skill) => (
                  <span
                    key={skill}
                    className="rounded-full px-2 py-1 text-xs"
                    style={{ background: "var(--accent-wash)", color: "var(--accent)" }}
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">No hires recorded yet.</p>
          )}
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Skill trends */}
        <Card>
          <h3>Skill Trends</h3>
          <p className="text-sm text-[var(--text-mute)]">
            Skills most frequently matched across your candidates.
          </p>
          {data.skill_trends.length > 0 ? (
            <ChartWell>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={data.skill_trends} layout="vertical">
                  <CartesianGrid horizontal={false} />
                  <XAxis type="number" allowDecimals={false} tickLine={false} axisLine={false} />
                  <YAxis
                    type="category"
                    dataKey="skill"
                    tickLine={false}
                    axisLine={false}
                    width={90}
                  />
                  <ChartTooltip />
                  <Bar dataKey="count" fill="var(--accent)" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartWell>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">No matched skills yet.</p>
          )}
        </Card>

        {/* Student skill-gap trends */}
        <Card>
          <h3>Student Skill-Gap Trends</h3>
          <p className="text-sm text-[var(--text-mute)]">
            Skills most frequently missing among candidates who applied.
          </p>
          {data.skill_gap_trends.length > 0 ? (
            <ChartWell>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={data.skill_gap_trends} layout="vertical">
                  <CartesianGrid horizontal={false} />
                  <XAxis type="number" allowDecimals={false} tickLine={false} axisLine={false} />
                  <YAxis
                    type="category"
                    dataKey="skill"
                    tickLine={false}
                    axisLine={false}
                    width={90}
                  />
                  <ChartTooltip />
                  <Bar dataKey="count" fill="var(--warn)" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartWell>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">No skill gaps recorded yet.</p>
          )}
        </Card>
      </div>

      {/* Recruitment-stage trends */}
      <Card>
        <h3>Recruitment-Stage Trends</h3>
        <p className="text-sm text-[var(--text-mute)]">
          Applications received per week across your job postings.
        </p>
        {data.stage_trends.length > 0 ? (
          <ChartWell>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data.stage_trends}>
                <CartesianGrid vertical={false} />
                <XAxis dataKey="period" tickLine={false} axisLine={false} />
                <YAxis allowDecimals={false} tickLine={false} axisLine={false} width={28} />
                <ChartTooltip />
                <Bar dataKey="applications" fill="var(--accent-deep)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartWell>
        ) : (
          <p className="text-sm text-[var(--text-mute)]">No applications yet.</p>
        )}
      </Card>

      {/* Historical company patterns */}
      <Card>
        <h3>Historical Company Patterns</h3>
        <p className="text-sm text-[var(--text-mute)]">
          Applications, hire rate, and average AI score per job posting.
        </p>
        <DataTable
          columns={companyColumns}
          rows={data.company_patterns.map((p) => ({ ...p, id: p.job_id }))}
          emptyText="No job postings with applications yet."
        />
      </Card>
    </>
  );
}
