import * as React from "react";
import { useNavigate } from "react-router-dom";
import { Search } from "lucide-react";
import {
  ApiError,
  applyToJob,
  getJobsPage,
  getMyApplications,
  toggleSaveJob,
  uploadResume,
  type Application,
  type ApplyValidation,
  type JobCard as JobCardData,
  type JobFilters,
  type JobsPageData,
} from "@/lib/api";
import {
  Badge,
  Button,
  Card,
  Dropzone,
  ErrorState,
  GlobalFooter,
  Input,
  LoadingState,
  Modal,
  StudentNavbar,
  Shell,
  SimpleSelect,
  StatCard,
} from "@/components";

const FILTER_GROUPS: {
  key: keyof JobFilters;
  label: string;
  optionsKey: keyof JobsPageData["filters"];
}[] = [
  { key: "company", label: "Company", optionsKey: "companies" },
  { key: "job_role", label: "Job Role", optionsKey: "job_roles" },
  { key: "location", label: "Location", optionsKey: "locations" },
  { key: "job_type", label: "Job Type", optionsKey: "job_types" },
  { key: "experience_level", label: "Experience Level", optionsKey: "experience_levels" },
];

const VISIBLE_LIMIT = 5;

export default function JobsPage() {
  const [page, setPage] = React.useState<JobsPageData | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [filters, setFilters] = React.useState<JobFilters>({});
  const [searchInput, setSearchInput] = React.useState("");
  const [myApplicationsOpen, setMyApplicationsOpen] = React.useState(false);
  const [pendingApplyJobId, setPendingApplyJobId] = React.useState<number | null>(null);
  const [validation, setValidation] = React.useState<ApplyValidation | null>(null);

  const load = React.useCallback((nextFilters: JobFilters) => {
    getJobsPage(nextFilters)
      .then((data) => {
        setPage(data);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load jobs." : "Network error.");
      });
  }, []);

  React.useEffect(() => {
    load(filters);
  }, [load, filters]);

  function toggleFilterValue(key: keyof JobFilters, value: string) {
    setFilters((prev) => {
      const current = (prev[key] as string[] | undefined) ?? [];
      const next = current.includes(value)
        ? current.filter((v) => v !== value)
        : [...current, value];
      return { ...prev, [key]: next };
    });
  }

  function handleSearch() {
    setFilters((prev) => ({ ...prev, search: searchInput.trim() || undefined }));
  }

  function handleClearAll() {
    setSearchInput("");
    setFilters({});
  }

  async function handleApply(jobId: number) {
    try {
      await applyToJob(jobId);
      load(filters);
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        const body = err.body as { detail?: ApplyValidation };
        setValidation(body.detail ?? null);
        setPendingApplyJobId(jobId);
      } else {
        setError("Could not submit your application. Please try again.");
      }
    }
  }

  async function handleSave(jobId: number) {
    await toggleSaveJob(jobId);
    load(filters);
  }

  async function handleResumeUploaded() {
    if (pendingApplyJobId === null) return;
    const jobId = pendingApplyJobId;
    setPendingApplyJobId(null);
    setValidation(null);
    await handleApply(jobId);
  }

  return (
    <Shell navbar={<StudentNavbar />} footer={<GlobalFooter />}>
      {!page && !error ? <LoadingState label="Loading jobs…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {page ? (
        <PageBody
          page={page}
          filters={filters}
          searchInput={searchInput}
          onSearchInputChange={setSearchInput}
          onSearch={handleSearch}
          onToggleFilter={toggleFilterValue}
          onClearAll={handleClearAll}
          onApply={handleApply}
          onSave={handleSave}
          onOpenMyApplications={() => setMyApplicationsOpen(true)}
        />
      ) : null}

      <MissingInfoModal
        open={validation !== null}
        validation={validation}
        onOpenChange={(open) => {
          if (!open) {
            setValidation(null);
            setPendingApplyJobId(null);
          }
        }}
        onResumeUploaded={handleResumeUploaded}
      />

      <MyApplicationsModal open={myApplicationsOpen} onOpenChange={setMyApplicationsOpen} />
    </Shell>
  );
}

function PageBody({
  page,
  filters,
  searchInput,
  onSearchInputChange,
  onSearch,
  onToggleFilter,
  onClearAll,
  onApply,
  onSave,
  onOpenMyApplications,
}: {
  page: JobsPageData;
  filters: JobFilters;
  searchInput: string;
  onSearchInputChange: (value: string) => void;
  onSearch: () => void;
  onToggleFilter: (key: keyof JobFilters, value: string) => void;
  onClearAll: () => void;
  onApply: (jobId: number) => void;
  onSave: (jobId: number) => void;
  onOpenMyApplications: () => void;
}) {
  return (
    <>
      {/* Header */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
        <div>
          <h2>Discover Opportunities</h2>
          <p className="mt-1 text-sm text-[var(--text-soft)]">
            Apply to real jobs, track your applications, and get closer to your dream career.
          </p>
        </div>
        <Card flat className="justify-center text-center">
          <p className="text-sm text-[var(--text-soft)] italic">
            “Opportunities don’t just happen, you prepare for them.”
          </p>
          <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
        </Card>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <StatCard label="Total Jobs" value={page.summary.total_jobs} />
        </Card>
        <Card>
          <StatCard label="Applied" value={page.summary.applied} />
        </Card>
        <Card>
          <StatCard label="Under Review" value={page.summary.under_review} />
        </Card>
        <Card>
          <StatCard label="Shortlisted" value={page.summary.shortlisted} accent />
        </Card>
      </div>

      {/* Search / sort / my applications + filters */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_280px] lg:items-start">
        <div className="flex flex-col gap-3">
          <div className="flex flex-wrap gap-2">
            <div className="relative min-w-[220px] flex-1">
              <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-[var(--text-mute)]" />
              <Input
                value={searchInput}
                onChange={(e) => onSearchInputChange(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && onSearch()}
                placeholder="Search jobs by company, role, skills, or keywords…"
                className="pl-9"
              />
            </div>
            <Button onClick={onSearch}>Search</Button>
            <Button variant="ghost" onClick={onOpenMyApplications}>
              My Applications
            </Button>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-[var(--text-mute)]">Sort by</span>
            <SimpleSelect
              options={[{ value: "newest", label: "Posted Date (Newest)" }]}
              value="newest"
              disabled
              className="!w-auto text-xs"
              onChange={() => {}}
            />
          </div>

          {page.jobs.length === 0 ? (
            <Card>
              <p className="text-sm text-[var(--text-mute)]">
                No jobs match your search and filters.
              </p>
            </Card>
          ) : (
            page.jobs.map((job) => (
              <JobCard key={job.id} job={job} onApply={onApply} onSave={onSave} />
            ))
          )}
        </div>

        <FiltersPanel
          filters={filters}
          page={page}
          onToggleFilter={onToggleFilter}
          onClearAll={onClearAll}
        />
      </div>
    </>
  );
}

function FiltersPanel({
  filters,
  page,
  onToggleFilter,
  onClearAll,
}: {
  filters: JobFilters;
  page: JobsPageData;
  onToggleFilter: (key: keyof JobFilters, value: string) => void;
  onClearAll: () => void;
}) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3>Filters</h3>
        <Button variant="ghost" onClick={onClearAll} className="!px-2 !py-1 text-xs">
          Clear All
        </Button>
      </div>
      {FILTER_GROUPS.map((group) => (
        <FilterGroup
          key={group.key}
          label={group.label}
          options={page.filters[group.optionsKey]}
          selected={(filters[group.key] as string[] | undefined) ?? []}
          onToggle={(value) => onToggleFilter(group.key, value)}
          searchable={group.key === "company"}
        />
      ))}
    </Card>
  );
}

function FilterGroup({
  label,
  options,
  selected,
  onToggle,
  searchable,
}: {
  label: string;
  options: string[];
  selected: string[];
  onToggle: (value: string) => void;
  searchable?: boolean;
}) {
  const [query, setQuery] = React.useState("");
  const [expanded, setExpanded] = React.useState(false);

  const filtered = query.trim()
    ? options.filter((o) => o.toLowerCase().includes(query.trim().toLowerCase()))
    : options;
  const visible = expanded ? filtered : filtered.slice(0, VISIBLE_LIMIT);

  return (
    <div className="flex flex-col gap-1.5 border-t border-[var(--border)] pt-3 first:border-t-0 first:pt-0">
      <span className="text-xs font-medium text-[var(--text-mute)]">{label}</span>
      {searchable ? (
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={`Search ${label.toLowerCase()}…`}
          className="text-xs"
        />
      ) : null}
      {visible.length === 0 ? (
        <p className="text-xs text-[var(--text-mute)]">No options yet.</p>
      ) : (
        visible.map((option) => (
          <label key={option} className="flex items-center gap-2 text-sm text-[var(--text-soft)]">
            <input
              type="checkbox"
              checked={selected.includes(option)}
              onChange={() => onToggle(option)}
              className="size-3.5"
            />
            {option}
          </label>
        ))
      )}
      {filtered.length > VISIBLE_LIMIT ? (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="self-start text-xs text-[var(--accent)]"
        >
          {expanded ? "Show less" : "Show more"}
        </button>
      ) : null}
    </div>
  );
}

function JobCard({
  job,
  onApply,
  onSave,
}: {
  job: JobCardData;
  onApply: (jobId: number) => void;
  onSave: (jobId: number) => void;
}) {
  const [expanded, setExpanded] = React.useState(false);
  const visibleSkills = expanded ? job.required_skills : job.required_skills.slice(0, 5);
  const remaining = job.required_skills.length - visibleSkills.length;

  return (
    <Card>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <span
            className="flex size-10 shrink-0 items-center justify-center rounded-full text-sm font-semibold"
            style={{ background: "var(--accent-wash)", color: "var(--accent)" }}
          >
            {job.company_name.charAt(0)}
          </span>
          <div>
            <h3>{job.job_title}</h3>
            <p className="text-sm text-[var(--text-soft)]">{job.company_name}</p>
          </div>
        </div>
        <div className="flex flex-col items-end gap-1 text-right">
          <span className="text-xs text-[var(--text-mute)]">{job.posted_relative}</span>
          <Badge variant={job.status === "Open" ? "ok" : "neutral"}>{job.status}</Badge>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 text-xs text-[var(--text-mute)]">
        {job.location ? <span>{job.location}</span> : null}
        {job.job_type ? <span>● {job.job_type}</span> : null}
        {job.work_mode ? <span>● {job.work_mode}</span> : null}
        <span>● {job.experience_required}</span>
      </div>

      {job.description ? (
        <p className="text-sm text-[var(--text-soft)]">{job.description}</p>
      ) : null}

      <div className="flex flex-wrap gap-2">
        {visibleSkills.map((skill) => (
          <Badge key={skill} variant="neutral">
            {skill}
          </Badge>
        ))}
        {!expanded && remaining > 0 ? (
          <button
            type="button"
            onClick={() => setExpanded(true)}
            className="text-xs text-[var(--accent)]"
          >
            +{remaining} more
          </button>
        ) : null}
      </div>

      <div className="flex items-center justify-between gap-3">
        <Button onClick={() => onApply(job.id)} disabled={job.has_applied}>
          {job.has_applied ? "Applied" : "Apply Now →"}
        </Button>
        <Button variant="ghost" onClick={() => onSave(job.id)}>
          {job.is_saved ? "Saved ✓" : "Save"}
        </Button>
      </div>
    </Card>
  );
}

function MissingInfoModal({
  open,
  validation,
  onOpenChange,
  onResumeUploaded,
}: {
  open: boolean;
  validation: ApplyValidation | null;
  onOpenChange: (open: boolean) => void;
  onResumeUploaded: () => void;
}) {
  const [uploading, setUploading] = React.useState(false);
  const [uploadError, setUploadError] = React.useState<string | null>(null);
  const needsResume = validation?.missing.some((m) => m.field === "resume") ?? false;

  async function handleFiles(files: File[]) {
    const file = files[0];
    if (!file) return;
    setUploading(true);
    setUploadError(null);
    try {
      await uploadResume(file);
      onResumeUploaded();
    } catch {
      setUploadError("Could not upload your resume. Please try a PDF file.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Required Information Missing">
      <div className="flex flex-col gap-4">
        {validation?.missing.map((item) => (
          <p key={item.field} className="text-sm text-[var(--text-soft)]">
            {item.reason}
          </p>
        ))}
        {needsResume ? (
          <>
            <Dropzone
              accept="application/pdf"
              onFiles={handleFiles}
              hint={uploading ? "Uploading…" : "Drop your resume (PDF) or click to browse"}
            />
            {uploadError ? <p className="text-sm text-[var(--danger)]">{uploadError}</p> : null}
          </>
        ) : null}
      </div>
    </Modal>
  );
}

const STATUS_BADGE: Record<string, "ok" | "hold" | "rejected" | "neutral"> = {
  Hired: "ok",
  Shortlisted: "ok",
  Disapproved: "rejected",
  "Not Selected": "rejected",
};

const DETAIL_STATUSES = new Set(["Disapproved", "Not Selected", "Hired"]);

function MyApplicationsModal({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const [applications, setApplications] = React.useState<Application[] | null>(null);
  const [resultApp, setResultApp] = React.useState<Application | null>(null);

  React.useEffect(() => {
    if (!open) return;
    getMyApplications()
      .then(setApplications)
      .catch(() => setApplications([]));
  }, [open]);

  return (
    <>
      <Modal open={open} onOpenChange={onOpenChange} title="My Applications">
        {applications === null ? (
          <LoadingState label="Loading your applications…" />
        ) : applications.length === 0 ? (
          <p className="text-sm text-[var(--text-mute)]">You haven't applied to any jobs yet.</p>
        ) : (
          <ul className="flex flex-col gap-3">
            {applications.map((app) => (
              <li key={app.id} className="flex items-center justify-between gap-3 text-sm">
                <div>
                  <p className="font-medium text-[var(--text)]">{app.job_title}</p>
                  <p className="text-xs text-[var(--text-mute)]">
                    {app.company_name} · {app.job_role}
                  </p>
                </div>
                <div className="text-right">
                  <Badge variant={STATUS_BADGE[app.status_label] ?? "hold"}>
                    {app.status_label}
                  </Badge>
                  {DETAIL_STATUSES.has(app.status_label) ? (
                    <Button
                      variant="ghost"
                      className="!mt-1 !px-2 !py-1 text-xs"
                      onClick={() => setResultApp(app)}
                    >
                      {app.status_label === "Hired" ? "View Details →" : "View Reason →"}
                    </Button>
                  ) : null}
                </div>
              </li>
            ))}
          </ul>
        )}
      </Modal>

      <ApplicationResultModal
        application={resultApp}
        onOpenChange={(open) => !open && setResultApp(null)}
      />
    </>
  );
}

function ApplicationResultModal({
  application,
  onOpenChange,
}: {
  application: Application | null;
  onOpenChange: (open: boolean) => void;
}) {
  const navigate = useNavigate();
  const isHired = application?.status_label === "Hired";
  const reason = application?.disapproval_reason ?? "";
  const skillGapMatch = reason.match(/^Skill Gap:\s*(.+)$/i);

  return (
    <Modal open={application !== null} onOpenChange={onOpenChange} title="Application Result">
      {application ? (
        <div className="flex flex-col gap-3 text-sm">
          <p className="text-base font-semibold text-[var(--text)]">{application.job_title}</p>
          <div>
            <p className="text-xs font-medium text-[var(--text-mute)]">Status</p>
            <Badge variant={isHired ? "ok" : "rejected"}>{application.status_label}</Badge>
          </div>
          {isHired ? (
            <p className="text-[var(--text-soft)]">
              Congratulations — you were selected for this role! This outcome also helps LOOP-MIND
              recognize strong candidates for similar roles in the future.
            </p>
          ) : (
            <>
              <div>
                <p className="text-xs font-medium text-[var(--text-mute)]">Reason</p>
                <p className="text-[var(--text-soft)]">
                  {skillGapMatch ? "Skill Gap" : reason || "No reason recorded."}
                </p>
              </div>
              {skillGapMatch ? (
                <div>
                  <p className="text-xs font-medium text-[var(--text-mute)]">Skill</p>
                  <p className="text-[var(--text-soft)]">{skillGapMatch[1]}</p>
                </div>
              ) : null}
            </>
          )}
          <div className="flex justify-end gap-2">
            {skillGapMatch ? (
              <Button
                variant="ghost"
                onClick={() => {
                  onOpenChange(false);
                  navigate("/app/skill-gap");
                }}
              >
                Go to Preparation →
              </Button>
            ) : null}
            <Button variant="ghost" onClick={() => onOpenChange(false)}>
              Close
            </Button>
          </div>
        </div>
      ) : null}
    </Modal>
  );
}
