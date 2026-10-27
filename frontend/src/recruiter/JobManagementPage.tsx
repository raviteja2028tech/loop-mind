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
  TagInput,
  Textarea,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import {
  ApiError,
  createRecruiterJob,
  getRecruiterJobsPage,
  setRecruiterJobStatus,
  type RecruiterJobRow,
  type RecruiterJobsPageData,
} from "@/lib/api";
import { RecruiterFooter } from "@/recruiter/RecruiterFooter";

const EXPERIENCE_OPTIONS = ["Entry Level", "Mid Level", "Senior Level"];
// Same vocabulary the seeded jobs and the student Jobs page filters
// already use (backend/core/seed_jobs.py) — kept consistent rather than
// inventing a second, differently-worded option set.
const JOB_TYPE_OPTIONS = ["Full-time", "Part-time", "Internship", "Contract"];
const WORK_MODE_OPTIONS = ["On-site", "Hybrid", "Remote"];
const STATUS_OPTIONS = [
  { value: "all", label: "All Status" },
  { value: "active", label: "Active" },
  { value: "paused", label: "Paused" },
];

export default function JobManagementPage() {
  const [page, setPage] = React.useState<RecruiterJobsPageData | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [search, setSearch] = React.useState("");
  const [status, setStatus] = React.useState("all");
  const [createOpen, setCreateOpen] = React.useState(false);
  const [detailJob, setDetailJob] = React.useState<RecruiterJobRow | null>(null);

  const load = React.useCallback(() => {
    getRecruiterJobsPage({ search: search || undefined, status })
      .then((data) => {
        setPage(data);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load your jobs." : "Network error.");
      });
  }, [search, status]);

  React.useEffect(() => {
    load();
  }, [load]);

  async function handleToggleStatus(job: RecruiterJobRow) {
    const next = job.status === "Active" ? "paused" : "active";
    await setRecruiterJobStatus(job.id, next);
    load();
  }

  const columns: Column<RecruiterJobRow & { id: number }>[] = [
    { key: "job_title", header: "Job Title", render: (r) => r.job_title },
    { key: "job_role", header: "Role Type", render: (r) => r.job_role },
    { key: "experience_required", header: "Experience", render: (r) => r.experience_required },
    { key: "applications", header: "Applications", render: (r) => r.applications },
    { key: "shortlisted", header: "Shortlisted", render: (r) => r.shortlisted },
    { key: "under_review", header: "Under Review", render: (r) => r.under_review },
    { key: "rejected", header: "Rejected", render: (r) => r.rejected },
    {
      key: "status",
      header: "Status",
      render: (r) => <Badge variant={r.status === "Active" ? "ok" : "neutral"}>{r.status}</Badge>,
    },
    { key: "posted", header: "Posted", render: (r) => r.posted_relative },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" className="!px-2 !py-1 text-xs" onClick={() => setDetailJob(r)}>
            View Details →
          </Button>
          <Button
            variant="ghost"
            className="!px-2 !py-1 text-xs"
            onClick={() => handleToggleStatus(r)}
          >
            ⋮ {r.status === "Active" ? "Pause" : "Activate"}
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
      {!page && !error ? <LoadingState label="Loading your jobs…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {page ? (
        <>
          {/* Header */}
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
            <div>
              <h2>Job Management</h2>
              <p className="mt-1 text-sm text-[var(--text-soft)]">
                Create, track, and manage all your job postings in one place.
              </p>
            </div>
            <Card flat className="justify-center text-center">
              <p className="text-sm text-[var(--text-soft)] italic">
                “Great teams build great products.”
              </p>
              <p className="text-xs text-[var(--text-mute)]">– LOOP-MIND</p>
            </Card>
          </div>

          {/* Stat cards */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Card>
              <StatCard label="Total Jobs" value={page.summary.total_jobs} />
            </Card>
            <Card>
              <StatCard label="Active Jobs" value={page.summary.active_jobs} accent />
            </Card>
            <Card>
              <StatCard label="Paused Jobs" value={page.summary.paused_jobs} />
            </Card>
            <Card>
              <StatCard label="Total Applications" value={page.summary.total_applications} />
            </Card>
          </div>

          {/* Your Job Postings */}
          <Card>
            <div className="flex flex-wrap items-start justify-between gap-3">
              <h3>Your Job Postings</h3>
              <div className="flex flex-wrap gap-2">
                <Input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search jobs by title, role, or keywords…"
                  className="min-w-[220px]"
                />
                <SimpleSelect
                  options={STATUS_OPTIONS}
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="!w-auto"
                />
                <Button onClick={() => setCreateOpen(true)}>+ Create New Job</Button>
              </div>
            </div>
            <DataTable
              columns={columns}
              rows={page.jobs.map((j) => ({ ...j, id: j.id }))}
              emptyText="No job postings yet. Create your first job to get started."
            />
          </Card>
        </>
      ) : null}

      <CreateJobModal open={createOpen} onOpenChange={setCreateOpen} onCreated={load} />

      <Modal
        open={detailJob !== null}
        onOpenChange={(open) => !open && setDetailJob(null)}
        title={detailJob ? detailJob.job_title : undefined}
      >
        {detailJob ? (
          <div className="flex flex-col gap-2 text-sm text-[var(--text-soft)]">
            <p>
              <strong>Company:</strong> {detailJob.company_name}
            </p>
            <p>
              <strong>Role:</strong> {detailJob.job_role}
            </p>
            <p>
              <strong>Experience:</strong> {detailJob.experience_required}
            </p>
            <p>
              <strong>Status:</strong> {detailJob.status} · {detailJob.posted_relative}
            </p>
            {detailJob.required_skills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {detailJob.required_skills.map((skill) => (
                  <Badge key={skill} variant="neutral">
                    {skill}
                  </Badge>
                ))}
              </div>
            ) : null}
            <p>
              <strong>Applications:</strong> {detailJob.applications} ·{" "}
              <strong>Shortlisted:</strong> {detailJob.shortlisted} · <strong>Under Review:</strong>{" "}
              {detailJob.under_review} · <strong>Rejected:</strong> {detailJob.rejected}
            </p>
          </div>
        ) : null}
      </Modal>
    </Shell>
  );
}

function CreateJobModal({
  open,
  onOpenChange,
  onCreated,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreated: () => void;
}) {
  const [companyName, setCompanyName] = React.useState("");
  const [jobTitle, setJobTitle] = React.useState("");
  const [jobRole, setJobRole] = React.useState("");
  const [experience, setExperience] = React.useState("");
  const [skills, setSkills] = React.useState<string[]>([]);
  const [jobType, setJobType] = React.useState("");
  const [workMode, setWorkMode] = React.useState("");
  const [location, setLocation] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const canSubmit = companyName.trim() && jobTitle.trim() && jobRole.trim() && experience;

  async function handleCreate() {
    if (!canSubmit) return;
    setSaving(true);
    setError(null);
    try {
      await createRecruiterJob({
        company_name: companyName.trim(),
        job_title: jobTitle.trim(),
        job_role: jobRole.trim(),
        experience_required: experience,
        required_skills: skills,
        job_type: jobType || null,
        work_mode: workMode || null,
        location: location.trim() || null,
        description: description.trim() || null,
      });
      onCreated();
      onOpenChange(false);
    } catch {
      setError("Could not create this job. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal
      key={String(open)}
      open={open}
      onOpenChange={onOpenChange}
      title="Create New Job"
      closeOnOverlayClick
    >
      <div className="flex flex-col gap-4">
        <div>
          <label className="lm-label">Company Name</label>
          <Input
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g. Acme Robotics"
          />
        </div>
        <div>
          <label className="lm-label">Job Title</label>
          <Input
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            placeholder="e.g. Software Engineer"
          />
        </div>
        <div>
          <label className="lm-label">Job Role</label>
          <Input
            value={jobRole}
            onChange={(e) => setJobRole(e.target.value)}
            placeholder="e.g. Backend Developer"
          />
        </div>
        <div>
          <label className="lm-label">Experience</label>
          <SimpleSelect
            options={EXPERIENCE_OPTIONS.map((o) => ({ value: o, label: o }))}
            value={experience}
            onChange={(e) => setExperience(e.target.value)}
            placeholder="Select experience level…"
          />
        </div>
        <div>
          <label className="lm-label">Job Constraints (required skills)</label>
          <TagInput value={skills} onChange={setSkills} placeholder="Type a skill, press Enter…" />
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label className="lm-label">Job Type</label>
            <SimpleSelect
              options={JOB_TYPE_OPTIONS.map((o) => ({ value: o, label: o }))}
              value={jobType}
              onChange={(e) => setJobType(e.target.value)}
              placeholder="Select job type…"
            />
          </div>
          <div>
            <label className="lm-label">Work Mode</label>
            <SimpleSelect
              options={WORK_MODE_OPTIONS.map((o) => ({ value: o, label: o }))}
              value={workMode}
              onChange={(e) => setWorkMode(e.target.value)}
              placeholder="Select work mode…"
            />
          </div>
        </div>
        <div>
          <label className="lm-label">Location</label>
          <Input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g. Bengaluru, India"
          />
        </div>
        <div>
          <label className="lm-label">Description</label>
          <Textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the role, responsibilities, and what a strong candidate looks like…"
            rows={4}
          />
        </div>
        {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
        <Button onClick={handleCreate} disabled={!canSubmit || saving} className="self-end">
          {saving ? "Creating…" : "Create Job"}
        </Button>
      </div>
    </Modal>
  );
}
