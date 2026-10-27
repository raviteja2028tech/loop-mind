import * as React from "react";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import { useNavigate } from "react-router-dom";
import {
  BarChart3,
  Briefcase,
  ChevronRight,
  Clock,
  FileText,
  MessageSquare,
  Plus,
  Users,
} from "lucide-react";
import { ApiError, getRecruiterDashboard, type RecruiterDashboardData } from "@/lib/api";
import {
  Badge,
  Button,
  Card,
  ChartTooltip,
  ChartWell,
  ErrorState,
  LoadingState,
  RecruiterNavbar,
  Shell,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import { RecruiterFooter } from "@/recruiter/RecruiterFooter";

const PIPELINE_COLORS = {
  shortlisted: "var(--accent)",
  under_review: "var(--warn)",
  rejected: "var(--accent-deep)",
} as const;

export default function RecruiterDashboard() {
  const [data, setData] = React.useState<RecruiterDashboardData | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getRecruiterDashboard()
      .then((d) => {
        setData(d);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load your dashboard." : "Network error.");
      });
  }, []);

  return (
    <Shell
      navbar={<RecruiterNavbar />}
      footer={<RecruiterFooter />}
    >
      {!data && !error ? <LoadingState label="Loading your dashboard…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {data ? <DashboardBody data={data} /> : null}
    </Shell>
  );
}

function DashboardBody({ data }: { data: RecruiterDashboardData }) {
  const navigate = useNavigate();
  const jobColumns: Column<RecruiterDashboardData["jobs"][number] & { id: number }>[] = [
    { key: "job_title", header: "Job Title", render: (r) => r.job_title },
    { key: "applications", header: "Applications", render: (r) => r.applications },
    { key: "shortlisted", header: "Shortlisted", render: (r) => r.shortlisted },
    { key: "under_review", header: "Under Review", render: (r) => r.under_review },
    { key: "rejected", header: "Rejected", render: (r) => r.rejected },
    {
      key: "status",
      header: "Status",
      render: (r) => <Badge variant={r.status === "Active" ? "ok" : "neutral"}>{r.status}</Badge>,
    },
    {
      key: "actions",
      header: "Actions",
      render: () => (
        <Button
          variant="ghost"
          className="!px-2 !py-1 text-xs"
          onClick={() => navigate("/recruiter/jobs")}
        >
          Manage
        </Button>
      ),
    },
  ];

  const applicationColumns: Column<
    RecruiterDashboardData["recent_applications"][number] & { id: number }
  >[] = [
    { key: "candidate_name", header: "Candidate Name", render: (r) => r.candidate_name },
    { key: "job_role", header: "Job Role", render: (r) => r.job_role },
    { key: "applied_on", header: "Applied On", render: (r) => r.applied_relative },
    {
      key: "ai_status",
      header: "AI Status",
      render: (r) => (
        <Badge variant={r.ai_status === "Pending" ? "neutral" : "hold"}>{r.ai_status}</Badge>
      ),
    },
    {
      key: "action",
      header: "Action",
      render: () => (
        <Button
          variant="ghost"
          className="!px-2 !py-1 text-xs"
          onClick={() => navigate("/recruiter/candidates")}
        >
          Review →
        </Button>
      ),
    },
  ];

  const interviewColumns: Column<
    RecruiterDashboardData["upcoming_interviews"][number] & { id: string }
  >[] = [
    { key: "candidate_name", header: "Candidate Name", render: (r) => r.candidate_name },
    { key: "job_role", header: "Job Role", render: (r) => r.job_role },
    {
      key: "scheduled_at",
      header: "Date & Time",
      render: (r) => new Date(r.scheduled_at).toLocaleString(),
    },
    { key: "status", header: "Status", render: (r) => <Badge variant="hold">{r.status}</Badge> },
  ];

  const pipelineData = [
    { key: "shortlisted", label: "Shortlisted", ...data.pipeline.shortlisted },
    { key: "under_review", label: "Under Review", ...data.pipeline.under_review },
    { key: "rejected", label: "Rejected", ...data.pipeline.rejected },
  ];
  const hasPipelineData = data.pipeline.total > 0;

  return (
    <>
      {/* Header */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
        <div>
          <h2>Welcome back, Recruiter!</h2>
          <p className="mt-1 text-sm text-[var(--text-soft)]">
            Manage your hiring process and find the right talent with AI-powered insights.
          </p>
        </div>
        <Card flat className="justify-center text-center">
          <p className="text-sm text-[var(--text-soft)] italic">
            “Great teams build great products.”
          </p>
          <p className="text-xs text-[var(--text-mute)]">– LOOP-MIND</p>
        </Card>
      </div>

      {/* Summary cards — Recruiter Dashboard — Final Specification §1:
         exactly these four, no separate Pending Approval card. */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <SummaryCard icon={Briefcase} label="Total Jobs" value={data.summary.total_jobs} />
        <SummaryCard
          icon={FileText}
          label="Total Applications"
          value={data.summary.total_applications}
        />
        <SummaryCard icon={Users} label="Shortlisted" value={data.summary.shortlisted} accent />
        <SummaryCard icon={Clock} label="Under Review" value={data.summary.under_review} />
      </div>

      {/* Your Jobs / Application Pipeline / Quick Actions */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1.4fr_1fr_0.9fr]">
        <Card>
          <div className="flex items-start justify-between gap-3">
            <div>
              <h3>Your Jobs</h3>
              <p className="text-sm text-[var(--text-mute)]">Manage and track your job postings.</p>
            </div>
            <div className="flex gap-2">
              <Button
                variant="ghost"
                className="!px-2 !py-1 text-xs"
                onClick={() => navigate("/recruiter/jobs")}
              >
                View all
              </Button>
              <Button className="!px-2 !py-1 text-xs" onClick={() => navigate("/recruiter/jobs")}>
                + Create New Job
              </Button>
            </div>
          </div>
          <DataTable
            columns={jobColumns}
            rows={data.jobs.map((j) => ({ ...j, id: j.id }))}
            emptyText="No job postings yet."
          />
        </Card>

        <Card>
          <h3>Application Pipeline</h3>
          <p className="text-sm text-[var(--text-mute)]">
            Overall application status across all jobs.
          </p>
          {hasPipelineData ? (
            <ChartWell>
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie
                    data={pipelineData}
                    dataKey="count"
                    nameKey="label"
                    innerRadius={45}
                    outerRadius={70}
                  >
                    {pipelineData.map((d) => (
                      <Cell
                        key={d.key}
                        fill={PIPELINE_COLORS[d.key as keyof typeof PIPELINE_COLORS]}
                      />
                    ))}
                  </Pie>
                  <ChartTooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartWell>
          ) : (
            <p className="text-sm text-[var(--text-mute)]">No applications yet.</p>
          )}
          <p className="text-center text-sm text-[var(--text-soft)]">
            <strong className="text-lg text-[var(--text)]">{data.pipeline.total}</strong>{" "}
            Applications
          </p>
          <ul className="flex flex-col gap-1 text-xs text-[var(--text-mute)]">
            {pipelineData.map((d) => (
              <li key={d.key} className="flex items-center gap-2">
                <span
                  className="inline-block size-2.5 rounded-full"
                  style={{ background: PIPELINE_COLORS[d.key as keyof typeof PIPELINE_COLORS] }}
                />
                {d.label}: {d.count} ({d.percentage}%)
              </li>
            ))}
          </ul>
        </Card>

        <Card>
          <h3>Quick Actions</h3>
          <Button className="justify-start gap-2" onClick={() => navigate("/recruiter/jobs")}>
            <Plus className="size-4" /> Create New Job →
          </Button>
          <Button
            variant="ghost"
            className="justify-start gap-2"
            onClick={() => navigate("/recruiter/candidates")}
          >
            <Users className="size-4" /> View All Candidates →
          </Button>
          <Button
            variant="ghost"
            className="justify-start gap-2"
            onClick={() => navigate("/recruiter/interviews")}
          >
            <MessageSquare className="size-4" /> Prepare Interview Questions →
          </Button>
          <Button
            variant="ghost"
            className="justify-start gap-2"
            onClick={() => navigate("/recruiter/analytics")}
          >
            <BarChart3 className="size-4" /> View Recruitment Analytics →
          </Button>
        </Card>
      </div>

      {/* Recent Applications / Upcoming Interviews */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <div className="flex items-center justify-between">
            <h3>Recent Applications</h3>
            <Button variant="ghost" disabled className="!px-2 !py-1 text-xs">
              View all
            </Button>
          </div>
          <DataTable
            columns={applicationColumns}
            rows={data.recent_applications.map((a) => ({ ...a, id: a.id }))}
            emptyText="No applications yet."
          />
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <h3>Upcoming Interviews</h3>
            <Button
              variant="ghost"
              className="!px-2 !py-1 text-xs"
              onClick={() => navigate("/recruiter/interviews")}
            >
              View all
            </Button>
          </div>
          <DataTable
            columns={interviewColumns}
            rows={data.upcoming_interviews.map((i, idx) => ({
              ...i,
              id: `${i.candidate_name}-${idx}`,
            }))}
            emptyText="No interviews scheduled yet."
          />
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <div className="flex items-center justify-between">
          <div>
            <h3>Recent Activity</h3>
            <p className="text-sm text-[var(--text-mute)]">
              Track the latest updates in your hiring process.
            </p>
          </div>
          <Button variant="ghost" disabled className="!px-2 !py-1 text-xs">
            View all
          </Button>
        </div>
        {data.recent_activity.length === 0 ? (
          <p className="text-sm text-[var(--text-mute)]">No activity yet.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {data.recent_activity.map((item, idx) => (
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
  );
}

function SummaryCard({
  icon: Icon,
  label,
  value,
  accent,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: number;
  accent?: boolean;
}) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <span
          className="flex size-9 items-center justify-center rounded-lg"
          style={{
            background: accent ? "var(--accent-wash)" : "var(--raised)",
            color: accent ? "var(--accent)" : "var(--text-mute)",
          }}
        >
          <Icon className="size-4" />
        </span>
        <ChevronRight className="size-4 text-[var(--text-mute)]" />
      </div>
      <span className="font-mono text-[10px] uppercase tracking-wide text-[var(--text-mute)]">
        {label}
      </span>
      <span
        className={
          "text-2xl font-semibold " + (accent ? "text-[var(--accent)]" : "text-[var(--text)]")
        }
      >
        {value}
      </span>
    </Card>
  );
}
