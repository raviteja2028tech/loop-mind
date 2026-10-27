import * as React from "react";
import { useNavigate } from "react-router-dom";
import {
  Badge,
  Button,
  Card,
  ErrorState,
  GlobalFooter,
  Input,
  Label,
  LoadingState,
  Modal,
  StudentNavbar,
  PhotoPicker,
  Shell,
  SimpleSelect,
  StatCard,
  TagInput,
  Textarea,
} from "@/components";
import { DataTable, type Column } from "@/components/Table";
import {
  ApiError,
  createCertification,
  createCodingExperience,
  createProject,
  createSkill,
  deleteAccount,
  deleteCertification,
  uploadCertificateFile,
  deleteCodingExperience,
  deleteProfilePhoto,
  deleteProject,
  deleteResume,
  deleteSkill,
  downloadProfilePhotoFile,
  downloadResumeFile,
  getAcademicInfo,
  getBasicInfo,
  getCareerPlacement,
  getConsent,
  getLearningPreparation,
  getProfessionalLinks,
  getProfilePage,
  getRecruitmentHistory,
  listCertifications,
  listCodingExperience,
  listProjects,
  listSkills,
  putAcademicInfo,
  putBasicInfo,
  putCareerPlacement,
  putConsent,
  putLearningPreparation,
  putProfessionalLinks,
  updateSkill,
  uploadProfilePhoto,
  uploadResume,
  type AcademicInfo,
  type BasicInfo,
  type CareerPlacement,
  type CodingExperience,
  type Consent,
  type LearningPreparation,
  type ProfessionalLinks,
  type ProfilePageData,
  type RecruitmentHistory,
  type StudentCertification,
  type StudentProject,
  type StudentSkill,
} from "@/lib/api";
import { useAuth } from "@/lib/auth";

const SECTIONS = [
  { key: "overview", label: "Overview" },
  { key: "basic", label: "Basic Information" },
  { key: "academics", label: "Academics" },
  { key: "skills", label: "Skills" },
  { key: "coding", label: "Coding Experience" },
  { key: "projects", label: "Projects" },
  { key: "certifications", label: "Certifications" },
  { key: "career", label: "Career & Placement" },
  { key: "learning", label: "Learning & Preparation" },
  { key: "interview", label: "Interview & Assessment" },
  { key: "links", label: "Professional Links & Resume" },
  { key: "history", label: "Recruitment History" },
  { key: "consent", label: "Consent & Knowledge Sharing" },
] as const;

type SectionKey = (typeof SECTIONS)[number]["key"];

/** My Profile UPDATE SDD §9-10: one "Save Changes" action, pinned to the
 * bottom-right of the page, that commits whichever editable section(s)
 * currently have unsaved changes — each section still owns its own local
 * Edit/Cancel and draft state (only its own fields, never someone else's,
 * are validated/persisted), it just no longer renders its own Save
 * button. Skills/Projects/Certifications/Coding Experience/Consent are
 * intentionally not registered here — they already persist each change
 * immediately when the student acts (add/edit/delete/toggle), so there is
 * no "draft" for a page-wide Save to batch. */
type SaveRegistration = { dirty: boolean; save: () => Promise<void> };
const ProfileSaveContext = React.createContext<{
  register: (id: string, reg: SaveRegistration) => void;
  unregister: (id: string) => void;
} | null>(null);

function useRegisterSave(id: string, dirty: boolean, save: () => Promise<void>) {
  const ctx = React.useContext(ProfileSaveContext);
  React.useEffect(() => {
    if (!ctx) return;
    ctx.register(id, { dirty, save });
    return () => ctx.unregister(id);
  }, [ctx, id, dirty, save]);
}

/** My Profile UPDATE SDD §13: the stored resume is a server filesystem
 * path, not a browsable URL — this fetches it with the student's own
 * auth and hands the browser a same-origin blob URL to open. */
async function handleDownloadResume() {
  const blob = await downloadResumeFile();
  const url = URL.createObjectURL(blob);
  window.open(url, "_blank");
  setTimeout(() => URL.revokeObjectURL(url), 30_000);
}

export default function MyProfilePage() {
  const [page, setPage] = React.useState<ProfilePageData | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [section, setSection] = React.useState<SectionKey>("overview");
  const [deleteOpen, setDeleteOpen] = React.useState(false);
  const [registry, setRegistry] = React.useState<Record<string, SaveRegistration>>({});
  const [savingAll, setSavingAll] = React.useState(false);
  const navigate = useNavigate();
  const { logout } = useAuth();

  const saveCtx = React.useMemo(
    () => ({
      register: (id: string, reg: SaveRegistration) =>
        setRegistry((r) => ({ ...r, [id]: reg })),
      unregister: (id: string) =>
        setRegistry((r) => {
          const { [id]: _removed, ...rest } = r;
          return rest;
        }),
    }),
    [],
  );
  const anyDirty = Object.values(registry).some((r) => r.dirty);

  async function handleSaveAll() {
    setSavingAll(true);
    try {
      // Sequential, not Promise.all: Learning & Preparation and Interview
      // & Assessment each independently fetch and PUT the *same*
      // underlying record — saving them concurrently could let one
      // overwrite the other's just-saved fields with its own stale copy.
      for (const r of Object.values(registry)) {
        if (r.dirty) await r.save();
      }
    } finally {
      setSavingAll(false);
    }
  }

  const load = React.useCallback(() => {
    getProfilePage()
      .then((data) => {
        setPage(data);
        setError(null);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? "Could not load your profile." : "Network error.");
      });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  async function handleDeleteConfirmed() {
    await deleteAccount();
    setDeleteOpen(false);
    logout();
    navigate("/");
  }

  return (
    <ProfileSaveContext.Provider value={saveCtx}>
    <Shell
      navbar={<StudentNavbar />}
      footer={<GlobalFooter />}
      sidebar={
        <div className="lm-sidebar">
          {SECTIONS.map((s) => (
            <button
              key={s.key}
              type="button"
              className={`lm-sidebar__item ${section === s.key ? "is-active" : ""}`}
              onClick={() => setSection(s.key)}
            >
              {s.label}
            </button>
          ))}
        </div>
      }
    >
      {!page && !error ? <LoadingState label="Loading your profile…" /> : null}
      {error ? <ErrorState message={error} /> : null}
      {page ? (
        <>
          {/* Header */}
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_320px]">
            <div>
              <h2>My Profile</h2>
              <p className="mt-1 text-sm text-[var(--text-soft)]">
                Manage your profile, track your progress, and keep your information up to date.
              </p>
            </div>
            <Card flat className="justify-center text-center">
              <p className="text-sm text-[var(--text-soft)] italic">
                “A better you today, a brighter tomorrow.”
              </p>
              <p className="text-xs text-[var(--text-mute)]">— LOOP-MIND</p>
            </Card>
          </div>

          {section === "overview" ? <OverviewSection page={page} onChanged={load} /> : null}
          {section === "basic" ? <BasicInfoCard onChanged={load} /> : null}
          {section === "academics" ? <AcademicsSection onChanged={load} /> : null}
          {section === "skills" ? <SkillsCard onChanged={load} /> : null}
          {section === "coding" ? <CodingExperienceCard /> : null}
          {section === "projects" ? <ProjectsCard onChanged={load} /> : null}
          {section === "certifications" ? <CertificationsCard onChanged={load} /> : null}
          {section === "career" ? <CareerPlacementCard onChanged={load} /> : null}
          {section === "learning" ? <LearningPreparationCard onChanged={load} /> : null}
          {section === "interview" ? <InterviewAssessmentCard onChanged={load} /> : null}
          {section === "links" ? <ProfessionalLinksCard onChanged={load} /> : null}
          {section === "history" ? <RecruitmentHistorySection /> : null}
          {section === "consent" ? <ConsentCard onChanged={load} /> : null}

          {/* Bottom action area — My Profile UPDATE SDD §9: Save Changes
             pinned bottom-right, next to the existing Delete Profile
             action. */}
          <div className="flex items-center justify-between">
            <Button variant="danger" onClick={() => setDeleteOpen(true)}>
              Delete Profile
            </Button>
            <Button onClick={handleSaveAll} disabled={!anyDirty || savingAll}>
              {savingAll ? "Saving…" : "Save Changes"}
            </Button>
          </div>
        </>
      ) : null}

      <Modal open={deleteOpen} onOpenChange={setDeleteOpen} title="Delete Account">
        <div className="flex flex-col gap-4">
          <p className="text-sm text-[var(--text-soft)]">
            Are you sure you want to delete the account? This permanently removes your profile,
            skills, projects, certifications, and applications. This cannot be undone.
          </p>
          <div className="flex justify-end gap-2">
            <Button variant="ghost" onClick={() => setDeleteOpen(false)}>
              No
            </Button>
            <Button variant="danger" onClick={handleDeleteConfirmed}>
              Yes
            </Button>
          </div>
        </div>
      </Modal>
    </Shell>
    </ProfileSaveContext.Provider>
  );
}

/** My Profile UPDATE SDD §4: the stored photo is a server filesystem
 * path — fetches it as a blob (same auth as everything else) and renders
 * it as an actual `<img>` instead of a placeholder label. Re-fetches
 * whenever `photoPath` changes (upload/delete), and never renders a
 * previous student's now-stale blob URL. */
function ProfilePhoto({ photoPath, fallbackInitial }: { photoPath: string | null; fallbackInitial: string }) {
  const [url, setUrl] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (!photoPath) return;
    let objectUrl: string | null = null;
    downloadProfilePhotoFile().then((blob) => {
      objectUrl = URL.createObjectURL(blob);
      setUrl(objectUrl);
    });
    return () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [photoPath]);

  if (photoPath && url) {
    return <img src={url} alt="Profile" className="size-full object-cover" />;
  }
  return <span className="text-lg text-[var(--text-mute)]">{fallbackInitial}</span>;
}

function OverviewSection({ page, onChanged }: { page: ProfilePageData; onChanged: () => void }) {
  const navigate = useNavigate();
  const [missingOpen, setMissingOpen] = React.useState(false);
  const [photoUploading, setPhotoUploading] = React.useState(false);
  const [photoDeleting, setPhotoDeleting] = React.useState(false);

  async function handlePhotoFiles(files: File[]) {
    const file = files[0];
    if (!file) return;
    setPhotoUploading(true);
    try {
      await uploadProfilePhoto(file);
      onChanged();
    } finally {
      setPhotoUploading(false);
    }
  }

  async function handleDeletePhoto() {
    setPhotoDeleting(true);
    try {
      await deleteProfilePhoto();
      onChanged();
    } finally {
      setPhotoDeleting(false);
    }
  }

  return (
    <>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_220px]">
        <Card>
          <p className="text-xs font-medium text-[var(--text-mute)]">Student Profile</p>
          <div className="flex items-center gap-4">
            <div
              className="flex size-16 shrink-0 items-center justify-center overflow-hidden rounded-full"
              style={{ background: "var(--raised)" }}
            >
              <ProfilePhoto
                photoPath={page.overview.profile_photo_path}
                fallbackInitial={(page.overview.full_name ?? "?").charAt(0)}
              />
            </div>
            <div>
              <p className="text-lg font-semibold text-[var(--text)]">
                {page.overview.full_name ?? "Unnamed Student"}
              </p>
              <p className="text-sm text-[var(--text-soft)]">
                {page.overview.degree ?? "—"} · {page.overview.college ?? "—"}
              </p>
              <p className="text-sm text-[var(--text-mute)]">
                Semester {page.overview.current_semester ?? "—"} ·{" "}
                {[page.overview.city, page.overview.state].filter(Boolean).join(", ") || "—"}
              </p>
              <div className="mt-1 flex items-center gap-2">
                <PhotoPicker
                  onFiles={handlePhotoFiles}
                  trigger={
                    <Button variant="ghost" className="!px-2 !py-1 text-xs" disabled={photoUploading}>
                      {photoUploading
                        ? "Uploading…"
                        : page.overview.profile_photo_path
                          ? "Change Photo"
                          : "Upload Photo"}
                    </Button>
                  }
                />
                {page.overview.profile_photo_path ? (
                  <Button
                    variant="ghost"
                    className="!px-2 !py-1 text-xs"
                    disabled={photoDeleting}
                    onClick={() => void handleDeletePhoto()}
                  >
                    {photoDeleting ? "Deleting…" : "Delete Photo"}
                  </Button>
                ) : null}
              </div>
            </div>
          </div>
        </Card>
        <Card className="items-center text-center">
          <p className="text-xs font-medium text-[var(--text-mute)]">Profile Completion</p>
          <p className="text-3xl font-semibold text-[var(--accent)]">
            {page.completion_percentage}%
          </p>
          <Button
            variant="ghost"
            className="!px-2 !py-1 text-xs"
            onClick={() => setMissingOpen(true)}
          >
            View Missing Fields
          </Button>
        </Card>
      </div>

      <Card>
        <h3>Quick Actions</h3>
        <div className="flex flex-wrap gap-2">
          <Button variant="ghost" onClick={() => navigate("/app/profile/public")}>
            View Public Profile
          </Button>
          {/* My Profile UPDATE SDD §13: active exactly when a valid resume
             exists — not tied to job-application count, which was this
             button's previous (incorrect) gate. */}
          <Button
            variant="ghost"
            onClick={() => void handleDownloadResume()}
            disabled={!page.overview.has_resume}
          >
            Download Resume
          </Button>
          <Button variant="ghost" onClick={() => navigate("/app/skill-gap")}>
            View Placement Readiness
          </Button>
        </div>
      </Card>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <StatCard label="Skills Added" value={page.stats.skills_added} accent />
        </Card>
        <Card>
          <StatCard label="Projects" value={page.stats.projects} />
        </Card>
        <Card>
          <StatCard label="Certifications" value={page.stats.certifications} />
        </Card>
        <Card>
          <StatCard label="Job Applications" value={page.stats.job_applications} />
        </Card>
      </div>

      <BasicInfoCard onChanged={onChanged} />
      <AcademicsSection onChanged={onChanged} />
      <SkillsCard onChanged={onChanged} />

      <Modal open={missingOpen} onOpenChange={setMissingOpen} title="Missing Fields">
        {page.missing_fields.length === 0 ? (
          <p className="text-sm text-[var(--text-mute)]">Your profile is fully complete.</p>
        ) : (
          <ul className="flex flex-col gap-2 text-sm">
            {page.missing_fields.map((m, idx) => (
              <li key={idx} className="flex items-center justify-between gap-3">
                <span className="text-[var(--text-soft)]">{m.section}</span>
                <span className="text-[var(--text-mute)]">{m.field}</span>
              </li>
            ))}
          </ul>
        )}
      </Modal>
    </>
  );
}

/** Shared "Edit -> Save Changes (inactive until dirty) / Cancel" card
 * wrapper — spec.md My Profile §22-23. Each editable section owns its own
 * local edit/dirty state rather than one page-wide tracker across every
 * independent form; functionally equivalent, much simpler. */
/** My Profile UPDATE SDD §9: per-section Save Changes buttons were
 * replaced by the one page-level Save Changes action (bottom-right) — a
 * section being edited still shows its own Cancel (revert this section's
 * draft, exit edit mode) and a "Unsaved changes" hint so it's clear the
 * page-level button is what commits it. */
function EditableCard({
  title,
  protectedNote,
  children,
  editing,
  dirty,
  onEdit,
  onCancel,
  saving,
}: {
  title: string;
  protectedNote?: string;
  children: React.ReactNode;
  editing: boolean;
  dirty: boolean;
  onEdit: () => void;
  onCancel: () => void;
  saving: boolean;
}) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3>{title}</h3>
        {!editing ? (
          <Button variant="ghost" className="!px-2 !py-1 text-xs" onClick={onEdit}>
            Edit
          </Button>
        ) : null}
      </div>
      {protectedNote ? <p className="text-xs text-[var(--text-mute)]">{protectedNote}</p> : null}
      {children}
      {editing ? (
        <div className="flex items-center justify-end gap-3">
          {dirty && !saving ? (
            <p className="text-xs text-[var(--text-mute)]">
              Unsaved changes — use Save Changes below to commit.
            </p>
          ) : null}
          {saving ? <p className="text-xs text-[var(--text-mute)]">Saving…</p> : null}
          <Button variant="ghost" onClick={onCancel} disabled={saving}>
            Cancel
          </Button>
        </div>
      ) : null}
    </Card>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <Label>{label}</Label>
      {children}
    </div>
  );
}

function BasicInfoCard({ onChanged }: { onChanged: () => void }) {
  const [data, setData] = React.useState<BasicInfo | null>(null);
  const [draft, setDraft] = React.useState<BasicInfo | null>(null);
  const [editing, setEditing] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const load = React.useCallback(() => {
    getBasicInfo().then((d) => {
      setData(d);
      setDraft(d);
    });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const dirty = React.useMemo(() => JSON.stringify(data) !== JSON.stringify(draft), [data, draft]);

  const handleSave = React.useCallback(async () => {
    if (!draft) return;
    setSaving(true);
    try {
      const { profile_photo_path: _profilePhotoPath, ...payload } = draft;
      await putBasicInfo(payload);
      onChanged();
      load();
      setEditing(false);
    } finally {
      setSaving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draft]);
  useRegisterSave("basic-info", editing && dirty, handleSave);

  if (!data || !draft) {
    return (
      <Card>
        <h3>Basic Information</h3>
        <p className="text-sm text-[var(--text-mute)]">
          Complete onboarding to see your Basic Information here.
        </p>
      </Card>
    );
  }

  return (
    <EditableCard
      title="Basic Information"
      protectedNote="Full Name is part of your account and cannot be edited here."
      editing={editing}
      dirty={dirty}
      saving={saving}
      onEdit={() => setEditing(true)}
      onCancel={() => {
        setDraft(data);
        setEditing(false);
      }}
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <Field label="Full Name">
          <Input value={draft.full_name} disabled />
        </Field>
        <Field label="Date of Birth">
          <Input type="date" value={draft.date_of_birth} disabled={!editing} readOnly />
        </Field>
        <Field label="Gender">
          <Input value={draft.gender} disabled={!editing} readOnly />
        </Field>
        <Field label="Email">
          <Input
            value={draft.email}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, email: e.target.value })}
          />
        </Field>
        <Field label="Country">
          <Input
            value={draft.country}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, country: e.target.value })}
          />
        </Field>
        <Field label="State">
          <Input
            value={draft.state}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, state: e.target.value })}
          />
        </Field>
        <Field label="City">
          <Input
            value={draft.city}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, city: e.target.value })}
          />
        </Field>
        <Field label="Alternate Mobile Number">
          <Input
            value={draft.alternate_mobile_number ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, alternate_mobile_number: e.target.value })}
          />
        </Field>
        <Field label="Postal/ZIP Code">
          <Input
            value={draft.postal_code ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, postal_code: e.target.value })}
          />
        </Field>
        <Field label="Current Location">
          <Input
            value={draft.current_location ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, current_location: e.target.value })}
          />
        </Field>
        <Field label="Permanent Location">
          <Input
            value={draft.permanent_location ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, permanent_location: e.target.value })}
          />
        </Field>
      </div>
    </EditableCard>
  );
}

function AcademicsSection({ onChanged }: { onChanged: () => void }) {
  return (
    <>
      <AcademicInfoCard onChanged={onChanged} />
      <AcademicPerformanceCard onChanged={onChanged} />
    </>
  );
}

function AcademicInfoCard({ onChanged }: { onChanged: () => void }) {
  const [data, setData] = React.useState<AcademicInfo | null>(null);
  const [draft, setDraft] = React.useState<AcademicInfo | null>(null);
  const [editing, setEditing] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const load = React.useCallback(() => {
    getAcademicInfo().then((d) => {
      setData(d);
      setDraft(d);
    });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const dirty = React.useMemo(() => JSON.stringify(data) !== JSON.stringify(draft), [data, draft]);

  const handleSave = React.useCallback(async () => {
    if (!draft) return;
    setSaving(true);
    try {
      await putAcademicInfo(draft);
      onChanged();
      load();
      setEditing(false);
    } finally {
      setSaving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draft]);
  useRegisterSave("academic-info", editing && dirty, handleSave);

  if (!data || !draft) {
    return (
      <Card>
        <h3>Academic Information</h3>
        <p className="text-sm text-[var(--text-mute)]">
          Complete onboarding to see your Academic Information here.
        </p>
      </Card>
    );
  }

  return (
    <EditableCard
      title="Academic Information"
      protectedNote="College/University, Branch/Department and Degree are part of your
        verified academic record and cannot be edited here."
      editing={editing}
      dirty={dirty}
      saving={saving}
      onEdit={() => setEditing(true)}
      onCancel={() => {
        setDraft(data);
        setEditing(false);
      }}
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <Field label="College/University">
          <Input value={draft.college} disabled />
        </Field>
        <Field label="College Location">
          <Input
            value={draft.college_location ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, college_location: e.target.value })}
          />
        </Field>
        <Field label="Degree">
          <Input value={draft.degree} disabled />
        </Field>
        <Field label="Branch/Department">
          <Input value={draft.branch} disabled />
        </Field>
        <Field label="Specialization">
          <Input
            value={draft.specialization ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, specialization: e.target.value })}
          />
        </Field>
        <Field label="Academic Year">
          <Input
            value={draft.academic_year}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, academic_year: e.target.value })}
          />
        </Field>
        <Field label="Current Year">
          <Input
            value={draft.current_year}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, current_year: e.target.value })}
          />
        </Field>
        <Field label="Current Semester">
          <Input
            value={draft.current_semester}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, current_semester: e.target.value })}
          />
        </Field>
        <Field label="Admission Year">
          <Input
            value={draft.admission_year}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, admission_year: e.target.value })}
          />
        </Field>
        <Field label="Expected Graduation Year">
          <Input
            value={draft.expected_graduation_year}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, expected_graduation_year: e.target.value })}
          />
        </Field>
      </div>
    </EditableCard>
  );
}

function AcademicPerformanceCard({ onChanged }: { onChanged: () => void }) {
  const [data, setData] = React.useState<AcademicInfo | null>(null);
  const [draft, setDraft] = React.useState<AcademicInfo | null>(null);
  const [editing, setEditing] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const load = React.useCallback(() => {
    getAcademicInfo().then((d) => {
      setData(d);
      setDraft(d);
    });
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const dirty = React.useMemo(() => JSON.stringify(data) !== JSON.stringify(draft), [data, draft]);

  const handleSave = React.useCallback(async () => {
    if (!draft) return;
    setSaving(true);
    try {
      await putAcademicInfo(draft);
      onChanged();
      load();
      setEditing(false);
    } finally {
      setSaving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draft]);
  useRegisterSave("academic-performance", editing && dirty, handleSave);

  if (!data || !draft) return null;

  return (
    <EditableCard
      title="Academic Performance"
      editing={editing}
      dirty={dirty}
      saving={saving}
      onEdit={() => setEditing(true)}
      onCancel={() => {
        setDraft(data);
        setEditing(false);
      }}
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <Field label="Current CGPA">
          <Input
            type="number"
            step="0.01"
            value={draft.current_cgpa}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, current_cgpa: Number(e.target.value) })}
          />
        </Field>
        <Field label="CGPA Scale">
          <Input
            value={draft.cgpa_scale}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, cgpa_scale: e.target.value })}
          />
        </Field>
        <Field label="Academic Percentage">
          <Input
            type="number"
            value={draft.academic_percentage ?? ""}
            disabled={!editing}
            onChange={(e) =>
              setDraft({ ...draft, academic_percentage: Number(e.target.value) || null })
            }
          />
        </Field>
        <Field label="10th Score (%)">
          <Input
            type="number"
            value={draft.tenth_score_percentage ?? ""}
            disabled={!editing}
            onChange={(e) =>
              setDraft({ ...draft, tenth_score_percentage: Number(e.target.value) || null })
            }
          />
        </Field>
        <Field label="12th/Diploma Score (%)">
          <Input
            type="number"
            value={draft.twelfth_score_percentage ?? ""}
            disabled={!editing}
            onChange={(e) =>
              setDraft({ ...draft, twelfth_score_percentage: Number(e.target.value) || null })
            }
          />
        </Field>
        <Field label="Backlogs/Active Backlogs">
          <Input
            type="number"
            value={draft.backlogs ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, backlogs: Number(e.target.value) || null })}
          />
        </Field>
        <Field label="Semester-wise SGPA (comma-separated)">
          <Input
            value={(draft.semester_wise_sgpa ?? []).join(", ")}
            disabled={!editing}
            onChange={(e) =>
              setDraft({
                ...draft,
                semester_wise_sgpa: e.target.value
                  .split(",")
                  .map((v) => Number(v.trim()))
                  .filter((v) => !Number.isNaN(v)),
              })
            }
          />
        </Field>
      </div>
    </EditableCard>
  );
}

function SkillsCard({ onChanged }: { onChanged: () => void }) {
  const [skills, setSkills] = React.useState<StudentSkill[] | null>(null);
  const [addOpen, setAddOpen] = React.useState(false);
  const [editTarget, setEditTarget] = React.useState<StudentSkill | null>(null);

  const load = React.useCallback(() => {
    listSkills().then(setSkills);
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  async function handleDelete(id: number) {
    await deleteSkill(id);
    load();
    onChanged();
  }

  const columns: Column<StudentSkill & { id: number }>[] = [
    { key: "skill_name", header: "Skill Name", render: (r) => r.skill_name },
    { key: "skill_category", header: "Skill Category", render: (r) => r.skill_category },
    { key: "proficiency", header: "Proficiency Level", render: (r) => r.proficiency },
    { key: "learning_status", header: "Learning Status", render: (r) => r.learning_status },
    {
      key: "experience_years",
      header: "Experience",
      render: (r) => (r.experience_years !== null ? `${r.experience_years} yrs` : "—"),
    },
    {
      key: "evidence",
      header: "Evidence",
      render: (r) => (r.evidence.length > 0 ? `${r.evidence.length} item(s)` : "—"),
    },
    {
      key: "action",
      header: "Action",
      render: (r) => (
        <div className="flex gap-2">
          <Button variant="ghost" className="!px-2 !py-1 text-xs" onClick={() => setEditTarget(r)}>
            Edit
          </Button>
          <Button
            variant="danger"
            className="!px-2 !py-1 text-xs"
            onClick={() => handleDelete(r.id)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3>Skills</h3>
        <Button className="!px-2 !py-1 text-xs" onClick={() => setAddOpen(true)}>
          + Add Skill
        </Button>
      </div>
      <DataTable
        columns={columns}
        rows={(skills ?? []).map((s) => ({ ...s, id: s.id }))}
        emptyText="No skills added yet."
      />
      <SkillFormModal
        open={addOpen}
        onOpenChange={setAddOpen}
        onSaved={() => {
          load();
          onChanged();
        }}
      />
      <SkillFormModal
        open={editTarget !== null}
        initial={editTarget}
        onOpenChange={(open) => !open && setEditTarget(null)}
        onSaved={() => {
          load();
          onChanged();
          setEditTarget(null);
        }}
      />
    </Card>
  );
}

function SkillFormModal({
  open,
  initial,
  onOpenChange,
  onSaved,
}: {
  open: boolean;
  initial?: StudentSkill | null;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void;
}) {
  return (
    <Modal
      key={initial?.id ?? "new"}
      open={open}
      onOpenChange={onOpenChange}
      title={initial ? "Edit Skill" : "Add Skill"}
      closeOnOverlayClick
    >
      {open ? (
        <SkillFormBody
          key={initial?.id ?? "new"}
          initial={initial}
          onOpenChange={onOpenChange}
          onSaved={onSaved}
        />
      ) : null}
    </Modal>
  );
}

function SkillFormBody({
  initial,
  onOpenChange,
  onSaved,
}: {
  initial?: StudentSkill | null;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void;
}) {
  const [name, setName] = React.useState(initial?.skill_name ?? "");
  const [category, setCategory] = React.useState(initial?.skill_category ?? "");
  const [proficiency, setProficiency] = React.useState(initial?.proficiency ?? "Beginner");
  const [learningStatus, setLearningStatus] = React.useState(
    initial?.learning_status ?? "Learning",
  );
  const [saving, setSaving] = React.useState(false);

  async function handleSubmit() {
    if (!name.trim() || !category.trim()) return;
    setSaving(true);
    try {
      const payload = {
        skill_name: name.trim(),
        skill_category: category.trim(),
        proficiency,
        learning_status: learningStatus,
        experience_years: null,
      };
      if (initial) {
        await updateSkill(initial.id, payload);
      } else {
        await createSkill(payload);
      }
      onSaved();
      onOpenChange(false);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <Field label="Skill Name">
        <Input value={name} onChange={(e) => setName(e.target.value)} />
      </Field>
      <Field label="Skill Category">
        <Input value={category} onChange={(e) => setCategory(e.target.value)} />
      </Field>
      <Field label="Proficiency Level">
        <SimpleSelect
          options={["Beginner", "Intermediate", "Advanced"].map((v) => ({ value: v, label: v }))}
          value={proficiency}
          onChange={(e) => setProficiency(e.target.value)}
        />
      </Field>
      <Field label="Learning Status">
        <SimpleSelect
          options={["Learning", "Confident", "Mastered"].map((v) => ({ value: v, label: v }))}
          value={learningStatus}
          onChange={(e) => setLearningStatus(e.target.value)}
        />
      </Field>
      <Button onClick={handleSubmit} disabled={!name.trim() || !category.trim() || saving}>
        {saving ? "Saving…" : "Save"}
      </Button>
    </div>
  );
}

function CodingExperienceCard() {
  const [entries, setEntries] = React.useState<CodingExperience[] | null>(null);
  const [addOpen, setAddOpen] = React.useState(false);

  const load = React.useCallback(() => {
    listCodingExperience().then(setEntries);
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3>Coding Experience</h3>
        <Button className="!px-2 !py-1 text-xs" onClick={() => setAddOpen(true)}>
          + Add Entry
        </Button>
      </div>
      {!entries || entries.length === 0 ? (
        <p className="text-sm text-[var(--text-mute)]">No coding experience added yet.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {entries.map((e) => (
            <li
              key={e.id}
              className="flex items-center justify-between rounded-lg border border-[var(--border)] p-3 text-sm"
            >
              <div>
                <p className="text-[var(--text)]">{e.coding_experience ?? "—"}</p>
                <p className="text-xs text-[var(--text-mute)]">
                  {e.programming_languages.join(", ") || "No languages listed"} · DSA:{" "}
                  {e.dsa_experience ?? "—"}
                </p>
              </div>
              <Button
                variant="danger"
                className="!px-2 !py-1 text-xs"
                onClick={async () => {
                  await deleteCodingExperience(e.id);
                  load();
                }}
              >
                Delete
              </Button>
            </li>
          ))}
        </ul>
      )}
      <CodingExperienceModal open={addOpen} onOpenChange={setAddOpen} onSaved={load} />
    </Card>
  );
}

function CodingExperienceModal({
  open,
  onOpenChange,
  onSaved,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void;
}) {
  const [codingExperience, setCodingExperience] = React.useState("");
  const [languages, setLanguages] = React.useState<string[]>([]);
  const [dsaExperience, setDsaExperience] = React.useState("");
  const [githubLink, setGithubLink] = React.useState("");
  const [saving, setSaving] = React.useState(false);

  async function handleSubmit() {
    setSaving(true);
    try {
      await createCodingExperience({
        coding_experience: codingExperience || null,
        programming_languages: languages,
        dsa_experience: dsaExperience || null,
        competitive_programming: null,
        coding_platforms: [],
        github_link: githubLink || null,
      });
      onSaved();
      onOpenChange(false);
      setCodingExperience("");
      setLanguages([]);
      setDsaExperience("");
      setGithubLink("");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal
      key={String(open)}
      open={open}
      onOpenChange={onOpenChange}
      title="Add Coding Experience"
      closeOnOverlayClick
    >
      <div className="flex flex-col gap-4">
        <Field label="Coding Experience">
          <Input value={codingExperience} onChange={(e) => setCodingExperience(e.target.value)} />
        </Field>
        <Field label="Programming Languages">
          <TagInput
            value={languages}
            onChange={setLanguages}
            placeholder="Type a language, press Enter…"
          />
        </Field>
        <Field label="DSA Experience">
          <Input value={dsaExperience} onChange={(e) => setDsaExperience(e.target.value)} />
        </Field>
        <Field label="GitHub Link">
          <Input value={githubLink} onChange={(e) => setGithubLink(e.target.value)} />
        </Field>
        <Button onClick={handleSubmit} disabled={saving}>
          {saving ? "Saving…" : "Save"}
        </Button>
      </div>
    </Modal>
  );
}

function ProjectsCard({ onChanged }: { onChanged: () => void }) {
  const [projects, setProjects] = React.useState<StudentProject[] | null>(null);
  const [addOpen, setAddOpen] = React.useState(false);

  const load = React.useCallback(() => {
    listProjects().then(setProjects);
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3>Projects</h3>
        <Button className="!px-2 !py-1 text-xs" onClick={() => setAddOpen(true)}>
          + Add Project
        </Button>
      </div>
      {!projects || projects.length === 0 ? (
        <p className="text-sm text-[var(--text-mute)]">No projects added yet.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {projects.map((p) => (
            <li
              key={p.id}
              className="flex items-center justify-between rounded-lg border border-[var(--border)] p-3 text-sm"
            >
              <div>
                <p className="text-[var(--text)]">{p.project_name}</p>
                <p className="text-xs text-[var(--text-mute)]">
                  {p.technologies_used.join(", ") || "No technologies listed"}
                </p>
              </div>
              <Button
                variant="danger"
                className="!px-2 !py-1 text-xs"
                onClick={async () => {
                  await deleteProject(p.id);
                  load();
                  onChanged();
                }}
              >
                Delete
              </Button>
            </li>
          ))}
        </ul>
      )}
      <ProjectModal
        open={addOpen}
        onOpenChange={setAddOpen}
        onSaved={() => {
          load();
          onChanged();
        }}
      />
    </Card>
  );
}

function ProjectModal({
  open,
  onOpenChange,
  onSaved,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void;
}) {
  const [name, setName] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [startDate, setStartDate] = React.useState("");
  const [endDate, setEndDate] = React.useState("");
  const [technologies, setTechnologies] = React.useState<string[]>([]);
  const [programmingLanguages, setProgrammingLanguages] = React.useState<string[]>([]);
  const [skillsDemonstrated, setSkillsDemonstrated] = React.useState<string[]>([]);
  const [studentRole, setStudentRole] = React.useState("");
  const [githubRepository, setGithubRepository] = React.useState("");
  const [liveDemo, setLiveDemo] = React.useState("");
  const [projectDocumentation, setProjectDocumentation] = React.useState("");
  const [projectEvidence, setProjectEvidence] = React.useState("");
  const [saving, setSaving] = React.useState(false);

  async function handleSubmit() {
    if (!name.trim()) return;
    setSaving(true);
    try {
      await createProject({
        project_name: name.trim(),
        project_description: description || null,
        project_type: null,
        project_status: null,
        start_date: startDate || null,
        end_date: endDate || null,
        technologies_used: technologies,
        programming_languages: programmingLanguages,
        frameworks: [],
        tools: [],
        skills_demonstrated: skillsDemonstrated,
        student_role: studentRole || null,
        team_or_individual: null,
        github_repository: githubRepository || null,
        live_demo: liveDemo || null,
        project_documentation: projectDocumentation || null,
        project_evidence: projectEvidence || null,
      });
      onSaved();
      onOpenChange(false);
      setName("");
      setDescription("");
      setStartDate("");
      setEndDate("");
      setTechnologies([]);
      setProgrammingLanguages([]);
      setSkillsDemonstrated([]);
      setStudentRole("");
      setGithubRepository("");
      setLiveDemo("");
      setProjectDocumentation("");
      setProjectEvidence("");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal
      key={String(open)}
      open={open}
      onOpenChange={onOpenChange}
      title="Add Project"
      closeOnOverlayClick
    >
      <div className="flex flex-col gap-4">
        <Field label="Project Name">
          <Input value={name} onChange={(e) => setName(e.target.value)} />
        </Field>
        <Field label="Project Description">
          <Textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} />
        </Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Start Date">
            <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </Field>
          <Field label="End Date">
            <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </Field>
        </div>
        <Field label="Technologies Used">
          <TagInput
            value={technologies}
            onChange={setTechnologies}
            placeholder="Type a technology, press Enter…"
          />
        </Field>
        <Field label="Programming Languages">
          <TagInput
            value={programmingLanguages}
            onChange={setProgrammingLanguages}
            placeholder="Type a language, press Enter…"
          />
        </Field>
        <Field label="Skills Demonstrated">
          <TagInput
            value={skillsDemonstrated}
            onChange={setSkillsDemonstrated}
            placeholder="Type a skill, press Enter…"
          />
        </Field>
        <Field label="Student's Role">
          <Input value={studentRole} onChange={(e) => setStudentRole(e.target.value)} />
        </Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="GitHub Repository">
            <Input value={githubRepository} onChange={(e) => setGithubRepository(e.target.value)} />
          </Field>
          <Field label="Live Demo">
            <Input value={liveDemo} onChange={(e) => setLiveDemo(e.target.value)} />
          </Field>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Project Documentation">
            <Input
              value={projectDocumentation}
              onChange={(e) => setProjectDocumentation(e.target.value)}
            />
          </Field>
          <Field label="Project Evidence">
            <Input value={projectEvidence} onChange={(e) => setProjectEvidence(e.target.value)} />
          </Field>
        </div>
        <Button onClick={handleSubmit} disabled={!name.trim() || saving}>
          {saving ? "Saving…" : "Save"}
        </Button>
      </div>
    </Modal>
  );
}

function CertificationsCard({ onChanged }: { onChanged: () => void }) {
  const [certifications, setCertifications] = React.useState<StudentCertification[] | null>(null);
  const [addOpen, setAddOpen] = React.useState(false);

  const load = React.useCallback(() => {
    listCertifications().then(setCertifications);
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3>Certifications</h3>
        <Button className="!px-2 !py-1 text-xs" onClick={() => setAddOpen(true)}>
          + Add Certification
        </Button>
      </div>
      {!certifications || certifications.length === 0 ? (
        <p className="text-sm text-[var(--text-mute)]">No certifications added yet.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {certifications.map((c) => (
            <li
              key={c.id}
              className="flex items-center justify-between rounded-lg border border-[var(--border)] p-3 text-sm"
            >
              <div>
                <p className="text-[var(--text)]">{c.certification_name}</p>
                <p className="text-xs text-[var(--text-mute)]">{c.issuing_organization ?? "—"}</p>
              </div>
              <div className="flex items-center gap-3">
                <label className="cursor-pointer text-xs text-[var(--accent)]">
                  {c.certificate_file_path ? "Replace File" : "Upload File"}
                  <input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    className="hidden"
                    onChange={async (e) => {
                      const file = e.target.files?.[0];
                      if (file) {
                        await uploadCertificateFile(c.id, file);
                        load();
                      }
                      e.target.value = "";
                    }}
                  />
                </label>
                <Button
                  variant="danger"
                  className="!px-2 !py-1 text-xs"
                  onClick={async () => {
                    await deleteCertification(c.id);
                    load();
                    onChanged();
                  }}
                >
                  Delete
                </Button>
              </div>
            </li>
          ))}
        </ul>
      )}
      <CertificationModal
        open={addOpen}
        onOpenChange={setAddOpen}
        onSaved={() => {
          load();
          onChanged();
        }}
      />
    </Card>
  );
}

function CertificationModal({
  open,
  onOpenChange,
  onSaved,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void;
}) {
  const [name, setName] = React.useState("");
  const [issuer, setIssuer] = React.useState("");
  const [issueDate, setIssueDate] = React.useState("");
  const [expiryDate, setExpiryDate] = React.useState("");
  const [credentialUrl, setCredentialUrl] = React.useState("");
  const [saving, setSaving] = React.useState(false);

  async function handleSubmit() {
    if (!name.trim()) return;
    setSaving(true);
    try {
      await createCertification({
        certification_name: name.trim(),
        issuing_organization: issuer || null,
        certification_type: null,
        issue_date: issueDate || null,
        expiry_date: expiryDate || null,
        credential_id: null,
        credential_url: credentialUrl || null,
        skills_covered: [],
      });
      onSaved();
      onOpenChange(false);
      setName("");
      setIssuer("");
      setIssueDate("");
      setExpiryDate("");
      setCredentialUrl("");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal
      key={String(open)}
      open={open}
      onOpenChange={onOpenChange}
      title="Add Certification"
      closeOnOverlayClick
    >
      <div className="flex flex-col gap-4">
        <Field label="Certification Name">
          <Input value={name} onChange={(e) => setName(e.target.value)} />
        </Field>
        <Field label="Issuing Organization">
          <Input value={issuer} onChange={(e) => setIssuer(e.target.value)} />
        </Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Issue Date">
            <Input type="date" value={issueDate} onChange={(e) => setIssueDate(e.target.value)} />
          </Field>
          <Field label="Expiry Date">
            <Input type="date" value={expiryDate} onChange={(e) => setExpiryDate(e.target.value)} />
          </Field>
        </div>
        <Field label="Credential URL">
          <Input value={credentialUrl} onChange={(e) => setCredentialUrl(e.target.value)} />
        </Field>
        <Button onClick={handleSubmit} disabled={!name.trim() || saving}>
          {saving ? "Saving…" : "Save"}
        </Button>
      </div>
    </Modal>
  );
}

function CareerPlacementCard({ onChanged }: { onChanged: () => void }) {
  const [data, setData] = React.useState<CareerPlacement | null>(null);
  const [draft, setDraft] = React.useState<CareerPlacement | null>(null);
  const [editing, setEditing] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const EMPTY: CareerPlacement = {
    career_interest: null,
    target_job_role: null,
    preferred_job_domain: null,
    target_company: null,
    target_role: null,
    preferred_technology_skill_area: [],
    placement_interest: null,
    internship_interest: null,
    preferred_job_type: null,
    preferred_work_location: null,
    preferred_country: null,
    preferred_state: null,
    preferred_city: null,
    remote_onsite_hybrid: null,
    preferred_industry: null,
    placement_status: null,
  };

  const load = React.useCallback(() => {
    getCareerPlacement().then((d) => {
      setData(d ?? EMPTY);
      setDraft(d ?? EMPTY);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const dirty = React.useMemo(() => JSON.stringify(data) !== JSON.stringify(draft), [data, draft]);

  const handleSave = React.useCallback(async () => {
    if (!draft) return;
    setSaving(true);
    try {
      await putCareerPlacement(draft);
      onChanged();
      load();
      setEditing(false);
    } finally {
      setSaving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draft]);
  useRegisterSave("career-placement", editing && dirty, handleSave);

  if (!draft) return null;

  return (
    <EditableCard
      title="Career & Placement"
      editing={editing}
      dirty={dirty}
      saving={saving}
      onEdit={() => setEditing(true)}
      onCancel={() => {
        setDraft(data);
        setEditing(false);
      }}
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <Field label="Career Interest">
          <Input
            value={draft.career_interest ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, career_interest: e.target.value })}
          />
        </Field>
        <Field label="Target Job Role">
          <Input
            value={draft.target_job_role ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, target_job_role: e.target.value })}
          />
        </Field>
        <Field label="Target Company">
          <Input
            value={draft.target_company ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, target_company: e.target.value })}
          />
        </Field>
        <Field label="Target Role">
          <Input
            value={draft.target_role ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, target_role: e.target.value })}
          />
        </Field>
        <Field label="Placement Interest">
          <Input
            value={draft.placement_interest ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, placement_interest: e.target.value })}
          />
        </Field>
        <Field label="Internship Interest">
          <Input
            value={draft.internship_interest ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, internship_interest: e.target.value })}
          />
        </Field>
        <Field label="Preferred Work Location">
          <Input
            value={draft.preferred_work_location ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, preferred_work_location: e.target.value })}
          />
        </Field>
        <Field label="Remote / On-site / Hybrid">
          <Input
            value={draft.remote_onsite_hybrid ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, remote_onsite_hybrid: e.target.value })}
          />
        </Field>
        <Field label="Preferred Industry">
          <Input
            value={draft.preferred_industry ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, preferred_industry: e.target.value })}
          />
        </Field>
      </div>
    </EditableCard>
  );
}

function LearningPreparationCard({ onChanged }: { onChanged: () => void }) {
  const EMPTY: LearningPreparation = {
    current_learning_areas: [],
    skills_currently_learning: [],
    learning_goals: [],
    areas_to_improve: [],
    current_preparation_status: null,
    previous_interview_experience: null,
    previous_assessment_experience: null,
    technical_interview_experience: null,
    coding_assessment_experience: null,
    interview_preparation_status: null,
    assessment_preparation_status: null,
  };
  const [data, setData] = React.useState<LearningPreparation | null>(null);
  const [draft, setDraft] = React.useState<LearningPreparation | null>(null);
  const [editing, setEditing] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const load = React.useCallback(() => {
    getLearningPreparation().then((d) => {
      setData(d ?? EMPTY);
      setDraft(d ?? EMPTY);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const dirty = React.useMemo(() => JSON.stringify(data) !== JSON.stringify(draft), [data, draft]);

  const handleSave = React.useCallback(async () => {
    if (!draft) return;
    setSaving(true);
    try {
      await putLearningPreparation(draft);
      onChanged();
      load();
      setEditing(false);
    } finally {
      setSaving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draft]);
  useRegisterSave("learning-preparation", editing && dirty, handleSave);

  if (!draft) return null;

  return (
    <EditableCard
      title="Learning & Preparation"
      editing={editing}
      dirty={dirty}
      saving={saving}
      onEdit={() => setEditing(true)}
      onCancel={() => {
        setDraft(data);
        setEditing(false);
      }}
    >
      <div className="flex flex-col gap-3">
        <Field label="Current Learning Areas">
          <TagInput
            value={draft.current_learning_areas}
            onChange={(v) => setDraft({ ...draft, current_learning_areas: v })}
            placeholder={editing ? "Type an area, press Enter…" : undefined}
          />
        </Field>
        <Field label="Areas They Want to Improve">
          <TagInput
            value={draft.areas_to_improve}
            onChange={(v) => setDraft({ ...draft, areas_to_improve: v })}
            placeholder={editing ? "Type an area, press Enter…" : undefined}
          />
        </Field>
        <Field label="Current Preparation Status">
          <Input
            value={draft.current_preparation_status ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, current_preparation_status: e.target.value })}
          />
        </Field>
      </div>
    </EditableCard>
  );
}

function InterviewAssessmentCard({ onChanged }: { onChanged: () => void }) {
  const EMPTY: LearningPreparation = {
    current_learning_areas: [],
    skills_currently_learning: [],
    learning_goals: [],
    areas_to_improve: [],
    current_preparation_status: null,
    previous_interview_experience: null,
    previous_assessment_experience: null,
    technical_interview_experience: null,
    coding_assessment_experience: null,
    interview_preparation_status: null,
    assessment_preparation_status: null,
  };
  const [data, setData] = React.useState<LearningPreparation | null>(null);
  const [draft, setDraft] = React.useState<LearningPreparation | null>(null);
  const [editing, setEditing] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const load = React.useCallback(() => {
    getLearningPreparation().then((d) => {
      setData(d ?? EMPTY);
      setDraft(d ?? EMPTY);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const dirty = React.useMemo(() => JSON.stringify(data) !== JSON.stringify(draft), [data, draft]);

  const handleSave = React.useCallback(async () => {
    if (!draft) return;
    setSaving(true);
    try {
      await putLearningPreparation(draft);
      onChanged();
      load();
      setEditing(false);
    } finally {
      setSaving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draft]);
  useRegisterSave("interview-assessment", editing && dirty, handleSave);

  if (!draft) return null;

  return (
    <EditableCard
      title="Interview & Assessment"
      editing={editing}
      dirty={dirty}
      saving={saving}
      onEdit={() => setEditing(true)}
      onCancel={() => {
        setDraft(data);
        setEditing(false);
      }}
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <Field label="Previous Interview Experience">
          <Textarea
            value={draft.previous_interview_experience ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, previous_interview_experience: e.target.value })}
            rows={2}
          />
        </Field>
        <Field label="Previous Assessment Experience">
          <Textarea
            value={draft.previous_assessment_experience ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, previous_assessment_experience: e.target.value })}
            rows={2}
          />
        </Field>
        <Field label="Technical Interview Experience">
          <Textarea
            value={draft.technical_interview_experience ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, technical_interview_experience: e.target.value })}
            rows={2}
          />
        </Field>
        <Field label="Coding Assessment Experience">
          <Textarea
            value={draft.coding_assessment_experience ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, coding_assessment_experience: e.target.value })}
            rows={2}
          />
        </Field>
        <Field label="Interview Preparation Status">
          <Input
            value={draft.interview_preparation_status ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, interview_preparation_status: e.target.value })}
          />
        </Field>
        <Field label="Assessment Preparation Status">
          <Input
            value={draft.assessment_preparation_status ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, assessment_preparation_status: e.target.value })}
          />
        </Field>
      </div>
    </EditableCard>
  );
}

function ProfessionalLinksCard({ onChanged }: { onChanged: () => void }) {
  const EMPTY: ProfessionalLinks = {
    github_url: null,
    linkedin_url: null,
    portfolio_website_url: null,
    coding_profile_url: null,
    other_professional_profile_url: null,
    resume_file_path: null,
  };
  const [data, setData] = React.useState<ProfessionalLinks | null>(null);
  const [draft, setDraft] = React.useState<ProfessionalLinks | null>(null);
  const [editing, setEditing] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const load = React.useCallback(() => {
    getProfessionalLinks().then((d) => {
      setData(d ?? EMPTY);
      setDraft(d ?? EMPTY);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const dirty = React.useMemo(() => JSON.stringify(data) !== JSON.stringify(draft), [data, draft]);

  const handleSave = React.useCallback(async () => {
    if (!draft) return;
    setSaving(true);
    try {
      const { resume_file_path: _resumeFilePath, ...payload } = draft;
      await putProfessionalLinks(payload);
      onChanged();
      load();
      setEditing(false);
    } finally {
      setSaving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draft]);
  useRegisterSave("professional-links", editing && dirty, handleSave);

  if (!draft) return null;

  return (
    <EditableCard
      title="Professional Links & Resume"
      editing={editing}
      dirty={dirty}
      saving={saving}
      onEdit={() => setEditing(true)}
      onCancel={() => {
        setDraft(data);
        setEditing(false);
      }}
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <Field label="GitHub URL">
          <Input
            value={draft.github_url ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, github_url: e.target.value })}
          />
        </Field>
        <Field label="LinkedIn URL">
          <Input
            value={draft.linkedin_url ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, linkedin_url: e.target.value })}
          />
        </Field>
        <Field label="Portfolio Website URL">
          <Input
            value={draft.portfolio_website_url ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, portfolio_website_url: e.target.value })}
          />
        </Field>
        <Field label="Coding Profile URL">
          <Input
            value={draft.coding_profile_url ?? ""}
            disabled={!editing}
            onChange={(e) => setDraft({ ...draft, coding_profile_url: e.target.value })}
          />
        </Field>
        <Field label="Resume">
          <ResumeManager
            resumeFilePath={draft.resume_file_path}
            onChanged={() => {
              load();
              onChanged();
            }}
          />
        </Field>
      </div>
    </EditableCard>
  );
}

/** Skill Gap/Profile Photo/Resume Management UPDATE SDD §6-9: full resume
 * management from My Profile — view (Download), Replace, new Upload, and
 * Delete, all through the same `/students/me/resume` endpoint (and now
 * `DELETE`) the Dashboard's own resume card and the Professional Links
 * onboarding step already use, so there is exactly one active resume
 * record regardless of which page touched it last. */
function ResumeManager({
  resumeFilePath,
  onChanged,
}: {
  resumeFilePath: string | null;
  onChanged: () => void;
}) {
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  async function handleFile(file: File | undefined) {
    if (!file) return;
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
      setError("Resume must be a PDF file.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await uploadResume(file);
      onChanged();
    } catch {
      setError("Could not upload resume. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  async function handleDelete() {
    setBusy(true);
    setError(null);
    try {
      await deleteResume();
      onChanged();
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-3">
        <p className="text-sm text-[var(--text-soft)]">
          {resumeFilePath ? "Resume uploaded." : "No resume uploaded yet."}
        </p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(e) => {
            void handleFile(e.target.files?.[0]);
            e.target.value = "";
          }}
        />
        {resumeFilePath ? (
          <>
            <Button
              variant="ghost"
              className="!px-2 !py-1 text-xs"
              disabled={busy}
              onClick={() => void handleDownloadResume()}
            >
              Download
            </Button>
            <Button
              variant="ghost"
              className="!px-2 !py-1 text-xs"
              disabled={busy}
              onClick={() => inputRef.current?.click()}
            >
              {busy ? "Working…" : "Replace"}
            </Button>
            <Button
              variant="danger"
              className="!px-2 !py-1 text-xs"
              disabled={busy}
              onClick={() => void handleDelete()}
            >
              Delete
            </Button>
          </>
        ) : (
          <Button
            variant="ghost"
            className="!px-2 !py-1 text-xs"
            disabled={busy}
            onClick={() => inputRef.current?.click()}
          >
            {busy ? "Uploading…" : "Upload Resume"}
          </Button>
        )}
      </div>
      {error ? <ErrorState message={error} /> : null}
    </div>
  );
}

function ConsentCard({ onChanged }: { onChanged: () => void }) {
  const EMPTY: Consent = {
    consent_use_information: false,
    consent_learning_experience: false,
    consent_anonymized_intelligence: false,
  };
  const [draft, setDraft] = React.useState<Consent>(EMPTY);
  const [saving, setSaving] = React.useState(false);

  const load = React.useCallback(() => {
    getConsent().then((d) => setDraft(d ?? EMPTY));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  async function handleToggle(key: keyof Consent) {
    const next = { ...draft, [key]: !draft[key] };
    setDraft(next);
    setSaving(true);
    try {
      await putConsent(next);
      onChanged();
    } finally {
      setSaving(false);
    }
  }

  return (
    <Card>
      <h3>Consent & Knowledge Sharing</h3>
      <p className="text-sm text-[var(--text-mute)]">
        Control how your information contributes to LOOP-MIND's intelligence.
      </p>
      <ul className="flex flex-col gap-3">
        <ConsentToggle
          label="Consent to use relevant information"
          checked={draft.consent_use_information}
          disabled={saving}
          onToggle={() => handleToggle("consent_use_information")}
        />
        <ConsentToggle
          label="Consent for learning/recruitment experience"
          checked={draft.consent_learning_experience}
          disabled={saving}
          onToggle={() => handleToggle("consent_learning_experience")}
        />
        <ConsentToggle
          label="Consent for anonymized/aggregated intelligence"
          checked={draft.consent_anonymized_intelligence}
          disabled={saving}
          onToggle={() => handleToggle("consent_anonymized_intelligence")}
        />
      </ul>
    </Card>
  );
}

function ConsentToggle({
  label,
  checked,
  disabled,
  onToggle,
}: {
  label: string;
  checked: boolean;
  disabled: boolean;
  onToggle: () => void;
}) {
  return (
    <li className="flex items-center justify-between gap-3 text-sm">
      <span className="text-[var(--text-soft)]">{label}</span>
      <Button
        variant={checked ? "primary" : "ghost"}
        className="!px-3 !py-1 text-xs"
        onClick={onToggle}
        disabled={disabled}
      >
        {checked ? "Enabled" : "Disabled"}
      </Button>
    </li>
  );
}

function RecruitmentHistorySection() {
  const [history, setHistory] = React.useState<RecruitmentHistory | null>(null);

  React.useEffect(() => {
    getRecruitmentHistory().then(setHistory);
  }, []);

  if (!history) {
    return <LoadingState label="Loading recruitment history…" />;
  }

  return (
    <Card>
      <h3>Recruitment History</h3>
      <p className="text-sm text-[var(--text-mute)]">
        Derived from your real job applications — companies, roles, stages, and outcomes.
      </p>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Applications" value={history.total_applications} accent />
        <StatCard label="Selected" value={history.selected_count} />
        <StatCard label="Rejected" value={history.rejected_count} />
        <StatCard label="Under Review / Hold" value={history.hold_count} />
      </div>
      {history.applications.length === 0 ? (
        <p className="text-sm text-[var(--text-mute)]">No applications yet.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {history.applications.map((a, idx) => (
            <li
              key={idx}
              className="flex items-center justify-between rounded-lg border border-[var(--border)] p-3 text-sm"
            >
              <div>
                <p className="text-[var(--text)]">
                  {a.company_name} — {a.job_role}
                </p>
                <p className="text-xs text-[var(--text-mute)]">{a.applied_relative}</p>
              </div>
              <Badge variant={a.outcome === "Hired" ? "ok" : a.outcome ? "rejected" : "hold"}>
                {a.recruitment_stage_reached}
              </Badge>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

/** My Profile UPDATE SDD §12: a real, working "View Public Profile"
 * action instead of the previous permanently-disabled placeholder — a
 * read-only preview of the same stored profile data (name, academics,
 * skills, projects, certifications), reusing the existing student-scoped
 * endpoints rather than any new agent/analysis logic. */
export function PublicProfileView() {
  const navigate = useNavigate();
  const [page, setPage] = React.useState<ProfilePageData | null>(null);
  const [skills, setSkills] = React.useState<StudentSkill[]>([]);
  const [projects, setProjects] = React.useState<StudentProject[]>([]);
  const [certifications, setCertifications] = React.useState<StudentCertification[]>([]);

  React.useEffect(() => {
    getProfilePage().then(setPage);
    listSkills().then(setSkills);
    listProjects().then(setProjects);
    listCertifications().then(setCertifications);
  }, []);

  if (!page) return <LoadingState label="Loading public profile…" />;

  return (
    <Shell navbar={<StudentNavbar />} footer={<GlobalFooter />}>
      <div className="flex items-center justify-between">
        <h2>Public Profile</h2>
        <Button variant="ghost" onClick={() => navigate("/app/profile")}>
          Back to My Profile
        </Button>
      </div>
      <Card>
        <p className="text-lg font-semibold text-[var(--text)]">
          {page.overview.full_name ?? "Unnamed Student"}
        </p>
        <p className="text-sm text-[var(--text-soft)]">
          {page.overview.degree ?? "—"} · {page.overview.college ?? "—"}
        </p>
        <p className="text-sm text-[var(--text-mute)]">
          {[page.overview.city, page.overview.state].filter(Boolean).join(", ") || "—"}
        </p>
      </Card>
      <Card>
        <h3>Skills</h3>
        {skills.length === 0 ? (
          <p className="text-sm text-[var(--text-mute)]">No skills added yet.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {skills.map((s) => (
              <Badge key={s.id}>{s.skill_name}</Badge>
            ))}
          </div>
        )}
      </Card>
      <Card>
        <h3>Projects</h3>
        {projects.length === 0 ? (
          <p className="text-sm text-[var(--text-mute)]">No projects added yet.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {projects.map((p) => (
              <li key={p.id} className="text-sm text-[var(--text-soft)]">
                {p.project_name}
              </li>
            ))}
          </ul>
        )}
      </Card>
      <Card>
        <h3>Certifications</h3>
        {certifications.length === 0 ? (
          <p className="text-sm text-[var(--text-mute)]">No certifications added yet.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {certifications.map((c) => (
              <li key={c.id} className="text-sm text-[var(--text-soft)]">
                {c.certification_name}
              </li>
            ))}
          </ul>
        )}
      </Card>
    </Shell>
  );
}
