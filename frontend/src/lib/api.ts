/**
 * Minimal REST client for the LOOP-MIND FastAPI backend.
 * Vite dev server proxies /api → http://localhost:8000 (see vite.config.ts).
 */

const AUTH_TOKEN_KEY = "loop-mind.auth-token";

export function getAuthToken(): string | null {
  try {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  } catch {
    return null;
  }
}

export function setAuthToken(token: string | null) {
  try {
    if (token) localStorage.setItem(AUTH_TOKEN_KEY, token);
    else localStorage.removeItem(AUTH_TOKEN_KEY);
  } catch {
    /* storage unavailable — non-fatal */
  }
}

export class ApiError extends Error {
  status: number;
  body: unknown;
  constructor(status: number, body: unknown) {
    super(`API request failed with status ${status}`);
    this.status = status;
    this.body = body;
  }
}

/** My Profile UPDATE SDD §13: the resume file lives at a server
 * filesystem path, never reachable by a plain unauthenticated link —
 * fetches the PDF with the same bearer auth as every other request, then
 * hands the caller a blob URL it can open/download. */
export async function downloadResumeFile(): Promise<Blob> {
  const token = getAuthToken();
  const headers = new Headers();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch("/api/students/me/resume/file", { headers });
  if (!res.ok) throw new ApiError(res.status, await res.text().catch(() => null));
  return res.blob();
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body && !(init.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`/api${path}`, { ...init, headers });
  const contentType = res.headers.get("content-type") ?? "";
  const data = contentType.includes("application/json")
    ? await res.json().catch(() => null)
    : await res.text();

  if (!res.ok) throw new ApiError(res.status, data);
  return data as T;
}

export interface HealthStatus {
  status: string;
  service: string;
}

export function getHealth() {
  return apiFetch<HealthStatus>("/health");
}

export type AuthPurpose = "login" | "register";
export type AccountRole = "student" | "recruiter" | "registration";

export interface SendOtpResponse {
  mobile_number: string;
  resend_available_in_seconds: number;
  dev_otp: string | null;
}

export interface AuthSuccessResponse {
  token: string;
  role: AccountRole;
  redirect: string;
}

export interface MeResponse {
  id: number;
  mobile_number: string;
  role: AccountRole;
}

export function sendOtp(mobile_number: string, purpose: AuthPurpose) {
  return apiFetch<SendOtpResponse>("/auth/send-otp", {
    method: "POST",
    body: JSON.stringify({ mobile_number, purpose }),
  });
}

export function verifyOtp(mobile_number: string, code: string, purpose: AuthPurpose) {
  return apiFetch<AuthSuccessResponse>("/auth/verify-otp", {
    method: "POST",
    body: JSON.stringify({ mobile_number, code, purpose }),
  });
}

export function getMe() {
  return apiFetch<MeResponse>("/auth/me");
}

// ---- Phase 05: Student Profile onboarding ----

export interface BasicInfo {
  full_name: string;
  date_of_birth: string;
  gender: string;
  email: string;
  country: string;
  state: string;
  city: string;
  alternate_mobile_number?: string | null;
  postal_code?: string | null;
  current_location?: string | null;
  permanent_location?: string | null;
  profile_photo_path: string | null;
}

export interface AcademicInfo {
  college: string;
  college_location?: string | null;
  degree: string;
  branch: string;
  specialization?: string | null;
  academic_year: string;
  current_year: string;
  current_semester: string;
  admission_year: string;
  expected_graduation_year: string;
  current_cgpa: number;
  cgpa_scale: string;
  academic_percentage?: number | null;
  tenth_score_percentage: number | null;
  twelfth_score_percentage: number | null;
  semester_wise_sgpa?: number[];
  backlogs?: number | null;
}

export interface SkillEvidence {
  id: number;
  description: string;
  link: string | null;
}

export interface StudentSkill {
  id: number;
  skill_name: string;
  skill_category: string;
  proficiency: string;
  learning_status: string;
  experience_years: number | null;
  evidence: SkillEvidence[];
}

export interface CodingExperience {
  id: number;
  coding_experience: string | null;
  programming_languages: string[];
  dsa_experience: string | null;
  competitive_programming: string | null;
  coding_platforms: string[];
  github_link: string | null;
}

export interface StudentProject {
  id: number;
  project_name: string;
  project_description: string | null;
  project_type: string | null;
  project_status: string | null;
  start_date: string | null;
  end_date: string | null;
  technologies_used: string[];
  programming_languages: string[];
  frameworks: string[];
  tools: string[];
  skills_demonstrated: string[];
  student_role: string | null;
  team_or_individual: string | null;
  github_repository: string | null;
  live_demo: string | null;
  project_documentation: string | null;
  project_evidence: string | null;
}

export interface StudentCertification {
  id: number;
  certification_name: string;
  issuing_organization: string | null;
  certification_type: string | null;
  issue_date: string | null;
  expiry_date: string | null;
  credential_id: string | null;
  credential_url: string | null;
  skills_covered: string[];
  certificate_file_path: string | null;
}

export interface OnboardingStatus {
  basic_info_complete: boolean;
  academic_info_complete: boolean;
  has_skills: boolean;
  has_coding_experience: boolean;
  has_projects: boolean;
  has_certifications: boolean;
}

export const getBasicInfo = () => apiFetch<BasicInfo | null>("/students/me/basic-info");
export const putBasicInfo = (data: Omit<BasicInfo, "profile_photo_path">) =>
  apiFetch<BasicInfo>("/students/me/basic-info", { method: "PUT", body: JSON.stringify(data) });

export async function uploadProfilePhoto(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiFetch<BasicInfo>("/students/me/basic-info/photo", {
    method: "POST",
    body: formData,
  });
}

export const deleteProfilePhoto = () =>
  apiFetch<BasicInfo>("/students/me/basic-info/photo", { method: "DELETE" });

/** My Profile UPDATE SDD §4: the stored photo is a server filesystem
 * path, never reachable by a plain unauthenticated `<img src>` — fetches
 * it with the same bearer auth as every other request and hands back a
 * blob the caller can put in an `<img>` via `URL.createObjectURL`. */
export async function downloadProfilePhotoFile(): Promise<Blob> {
  const token = getAuthToken();
  const headers = new Headers();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch("/api/students/me/basic-info/photo/file", { headers });
  if (!res.ok) throw new ApiError(res.status, await res.text().catch(() => null));
  return res.blob();
}

export interface LinkedInExtractionResult {
  skills_added: number;
  certifications_added: number;
  projects_added: number;
}

export const extractLinkedIn = (linkedinUrl: string | null, profileText: string) =>
  apiFetch<LinkedInExtractionResult>("/students/me/linkedin-extract", {
    method: "POST",
    body: JSON.stringify({ linkedin_url: linkedinUrl, profile_text: profileText }),
  });

export const getAcademicInfo = () => apiFetch<AcademicInfo | null>("/students/me/academic-info");
export const putAcademicInfo = (data: AcademicInfo) =>
  apiFetch<AcademicInfo>("/students/me/academic-info", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export const listSkills = () => apiFetch<StudentSkill[]>("/students/me/skills");
export const createSkill = (data: Omit<StudentSkill, "id" | "evidence">) =>
  apiFetch<StudentSkill>("/students/me/skills", { method: "POST", body: JSON.stringify(data) });
export const updateSkill = (id: number, data: Omit<StudentSkill, "id" | "evidence">) =>
  apiFetch<StudentSkill>(`/students/me/skills/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
export const deleteSkill = (id: number) =>
  apiFetch<void>(`/students/me/skills/${id}`, { method: "DELETE" });
export const addSkillEvidence = (skillId: number, data: Omit<SkillEvidence, "id">) =>
  apiFetch<SkillEvidence>(`/students/me/skills/${skillId}/evidence`, {
    method: "POST",
    body: JSON.stringify(data),
  });

export const listCodingExperience = () =>
  apiFetch<CodingExperience[]>("/students/me/coding-experience");
export const createCodingExperience = (data: Omit<CodingExperience, "id">) =>
  apiFetch<CodingExperience>("/students/me/coding-experience", {
    method: "POST",
    body: JSON.stringify(data),
  });
export const deleteCodingExperience = (id: number) =>
  apiFetch<void>(`/students/me/coding-experience/${id}`, { method: "DELETE" });

export const listProjects = () => apiFetch<StudentProject[]>("/students/me/projects");
export const createProject = (data: Omit<StudentProject, "id">) =>
  apiFetch<StudentProject>("/students/me/projects", {
    method: "POST",
    body: JSON.stringify(data),
  });
export const deleteProject = (id: number) =>
  apiFetch<void>(`/students/me/projects/${id}`, { method: "DELETE" });

export const listCertifications = () =>
  apiFetch<StudentCertification[]>("/students/me/certifications");
export const createCertification = (
  data: Omit<StudentCertification, "id" | "certificate_file_path">,
) =>
  apiFetch<StudentCertification>("/students/me/certifications", {
    method: "POST",
    body: JSON.stringify(data),
  });
export const deleteCertification = (id: number) =>
  apiFetch<void>(`/students/me/certifications/${id}`, { method: "DELETE" });
export async function uploadCertificateFile(certId: number, file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiFetch<StudentCertification>(`/students/me/certifications/${certId}/file`, {
    method: "POST",
    body: formData,
  });
}

export const getOnboardingStatus = () =>
  apiFetch<OnboardingStatus>("/students/me/onboarding-status");

// ---- Student Create Account UPDATE SDD: registration draft ----
//
// No real student account exists during registration — every onboarding
// step below stages its data on a temporary draft instead of the real
// profile tables (backend/services/registration_service.py). The real
// account, and every one of these sections' real rows, are created only
// by `createAccount()` after Basic Information + consent are both
// present.

export interface DraftSkill {
  skill_name: string;
  skill_category: string;
  proficiency: string;
  learning_status: string;
  experience_years: number | null;
  evidence: Omit<SkillEvidence, "id">[];
}

export interface RegistrationDraft {
  mobile_number: string;
  linkedin_url: string | null;
  profile_photo_path: string | null;
  resume_file_path: string | null;
  basic_info: Omit<BasicInfo, "profile_photo_path"> | null;
  academic_info: AcademicInfo | null;
  skills: DraftSkill[];
  coding_experience: Omit<CodingExperience, "id">[];
  projects: Omit<StudentProject, "id">[];
  certifications: Omit<StudentCertification, "id" | "certificate_file_path">[];
  career_placement: CareerPlacement | null;
  learning_preparation: LearningPreparation | null;
  professional_links: Omit<ProfessionalLinks, "resume_file_path"> | null;
  consent: Consent | null;
}

export const getDraft = () => apiFetch<RegistrationDraft>("/registration/draft");

export const putDraftBasicInfo = (data: Omit<BasicInfo, "profile_photo_path">) =>
  apiFetch<{ saved: boolean }>("/registration/draft/basic-info", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export async function uploadDraftPhoto(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiFetch<{ saved: boolean }>("/registration/draft/basic-info/photo", {
    method: "POST",
    body: formData,
  });
}

export const putDraftAcademicInfo = (data: AcademicInfo) =>
  apiFetch<{ saved: boolean }>("/registration/draft/academic-info", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export const putDraftSkills = (items: DraftSkill[]) =>
  apiFetch<{ saved: boolean }>("/registration/draft/skills", {
    method: "PUT",
    body: JSON.stringify(items),
  });

export const putDraftCodingExperience = (items: Omit<CodingExperience, "id">[]) =>
  apiFetch<{ saved: boolean }>("/registration/draft/coding-experience", {
    method: "PUT",
    body: JSON.stringify(items),
  });

export const putDraftProjects = (items: Omit<StudentProject, "id">[]) =>
  apiFetch<{ saved: boolean }>("/registration/draft/projects", {
    method: "PUT",
    body: JSON.stringify(items),
  });

export const putDraftCertifications = (
  items: Omit<StudentCertification, "id" | "certificate_file_path">[],
) =>
  apiFetch<{ saved: boolean }>("/registration/draft/certifications", {
    method: "PUT",
    body: JSON.stringify(items),
  });

export const putDraftCareerPlacement = (data: CareerPlacement) =>
  apiFetch<{ saved: boolean }>("/registration/draft/career-placement", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export const putDraftLearningPreparation = (data: LearningPreparation) =>
  apiFetch<{ saved: boolean }>("/registration/draft/learning-preparation", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export const putDraftProfessionalLinks = (data: Omit<ProfessionalLinks, "resume_file_path">) =>
  apiFetch<{ saved: boolean }>("/registration/draft/professional-links", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export interface DraftResumeResult {
  saved: boolean;
  skills_added: number;
  certifications_added: number;
  projects_added: number;
}

export async function uploadDraftResume(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiFetch<DraftResumeResult>("/registration/draft/resume", {
    method: "POST",
    body: formData,
  });
}

export const putDraftLinkedinUrl = (linkedinUrl: string) =>
  apiFetch<{ saved: boolean }>("/registration/draft/linkedin-url", {
    method: "PUT",
    body: JSON.stringify({ linkedin_url: linkedinUrl }),
  });

export const extractDraftLinkedIn = () =>
  apiFetch<LinkedInExtractionResult>("/registration/draft/linkedin-extract", { method: "POST" });

/** LinkedIn Profile Extraction UPDATE SDD: real "Sign In with LinkedIn"
 * (OpenID Connect) for name/email/photo, alongside (not instead of) the
 * best-effort extraction above for skills/certifications/projects.
 * `configured` is false whenever no real LinkedIn Developer app has been
 * set up for this deployment yet — the frontend must show that honestly,
 * never pretend the button works. */
export interface LinkedInOAuthConfig {
  configured: boolean;
  authorization_url: string | null;
}

export const getLinkedInOAuthConfig = () =>
  apiFetch<LinkedInOAuthConfig>("/registration/draft/linkedin/oauth-config");

export interface LinkedInOAuthIdentity {
  name: string | null;
  email: string | null;
  email_verified: boolean;
  has_photo: boolean;
}

export const submitLinkedInOAuthCode = (code: string) =>
  apiFetch<LinkedInOAuthIdentity>("/registration/draft/linkedin/oauth-callback", {
    method: "POST",
    body: JSON.stringify({ code }),
  });

export const putDraftConsent = (data: Consent) =>
  apiFetch<{ saved: boolean }>("/registration/draft/consent", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export interface CreateAccountResult {
  token: string;
  role: AccountRole;
  redirect: string;
}

export const createAccount = () =>
  apiFetch<CreateAccountResult>("/registration/create-account", { method: "POST" });

// ---- Phase 06: Student Intelligence ----

export interface SkillGapAnalysisResult {
  id: number;
  target_company: string | null;
  target_role: string | null;
  analysis: {
    readiness: { readiness_percentage: number; status_message: string };
    skill_gap: Record<string, unknown>;
  };
  created_at: string;
}

export const createSkillGapAnalysis = (company_name: string, target_role: string | null) =>
  apiFetch<SkillGapAnalysisResult>("/students/me/skill-gap-analysis", {
    method: "POST",
    body: JSON.stringify({ company_name, target_role }),
  });

// ---- Phase 07: Student Dashboard ----

export interface PlacementReadinessSummary {
  has_analysis: boolean;
  readiness_percentage: number | null;
  status_message: string | null;
}

export interface RecentActivityItem {
  label: string;
  detail: string | null;
  relative_time: string;
}

export interface PreparationJourneyStage {
  key: string;
  label: string;
  supporting_text: string;
  complete: boolean;
}

export interface UpcomingTask {
  label: string;
}

export interface RecommendationCard {
  title: string;
  type: string;
}

export interface StatsPoint {
  category: string;
  value: number;
}

export interface DashboardData {
  full_name: string;
  profile_completion_percentage: number;
  skills_count: number;
  projects_count: number;
  certifications_count: number;
  target_company: string | null;
  has_resume: boolean;
  placement_readiness: PlacementReadinessSummary;
  recent_activity: RecentActivityItem[];
  preparation_journey: PreparationJourneyStage[];
  upcoming_tasks: UpcomingTask[];
  recommended_for_you: RecommendationCard[];
  stats: StatsPoint[];
  updated_at: string;
}

export const getDashboard = () => apiFetch<DashboardData>("/students/me/dashboard");

export interface CurrentSkill {
  skill_name: string;
  proficiency: string;
  evidence_count: number;
}

export interface PlacementReadinessDetail {
  has_analysis: boolean;
  target_company: string | null;
  target_role: string | null;
  readiness_percentage: number | null;
  status_message: string | null;
  current_skills: CurrentSkill[];
  ready_skills: string[];
}

export const getPlacementReadinessDetail = () =>
  apiFetch<PlacementReadinessDetail>("/students/me/placement-readiness-detail");

export const getTargetCompany = () =>
  apiFetch<{ company_name: string | null }>("/students/me/target-company");

export const putTargetCompany = (company_name: string) =>
  apiFetch<{ company_name: string | null }>("/students/me/target-company", {
    method: "PUT",
    body: JSON.stringify({ company_name }),
  });

export const getCompanyOptions = () => apiFetch<{ name: string }[]>("/students/me/company-options");

// ---- Phase 08: Skill Gap Analysis & What-If ----

export interface SkillGapReadiness {
  has_analysis: boolean;
  readiness_percentage: number | null;
  status_message: string | null;
  supporting_text: string | null;
}

export interface SkillGapOverview {
  total_required_skills: number;
  skills_you_have: number;
  skills_to_improve: number;
  missing_evidence: number;
}

export interface SkillDistribution {
  already_strong: number;
  needs_improvement: number;
  missing: number;
  not_relevant: number;
}

export interface PriorityArea {
  rank: number;
  skill: string;
  impact: string;
}

export type SkillStatus = "Strong" | "To Improve" | "Missing" | "Not Relevant" | "Missing Evidence";

export interface SkillRow {
  skill: string;
  category: string;
  your_level: string;
  required_level: string;
  status: SkillStatus;
  priority: string | null;
  resources: string | null;
}

export interface SkillGapPage {
  target_company: string | null;
  target_role: string | null;
  company_options: string[];
  role_options: string[];
  readiness: SkillGapReadiness;
  overview: SkillGapOverview;
  distribution: SkillDistribution;
  priority_areas: PriorityArea[];
  skills: SkillRow[];
}

export const getSkillGapPage = () => apiFetch<SkillGapPage>("/students/me/skill-gap");

export const putSkillGapTarget = (company_name: string, target_role: string | null) =>
  apiFetch<SkillGapPage>("/students/me/skill-gap/target", {
    method: "PUT",
    body: JSON.stringify({ company_name, target_role }),
  });

export const getRoleOptions = (company_name: string) =>
  apiFetch<string[]>(
    `/students/me/skill-gap/role-options?company_name=${encodeURIComponent(company_name)}`,
  );

export interface PreparationPlanItem {
  skill: string;
  category: string;
  priority: string;
  horizon: string;
  action: string;
}

export interface PreparationPlanResult {
  id: number;
  target_company: string | null;
  target_role: string | null;
  version: number;
  status: string;
  plan: {
    target_company: string | null;
    target_role: string | null;
    horizon_summary: string;
    year_guidance: string;
    items: PreparationPlanItem[];
  };
  created_at: string;
}

export const createPreparationPlan = (company_name: string, target_role: string | null) =>
  apiFetch<PreparationPlanResult>("/students/me/preparation-plan", {
    method: "POST",
    body: JSON.stringify({ company_name, target_role }),
  });

export interface WhatIfAnswer {
  question: string;
  topic: string | null;
  relevant_to_target: boolean;
  is_top_priority: boolean;
  answer: string;
  current_readiness_percentage: number | null;
  projected_readiness_percentage: number | null;
  relevant_roles: string[];
}

export interface WhatIfResult {
  id: number;
  question: string;
  result: WhatIfAnswer;
  created_at: string;
}

export const askWhatIf = (company_name: string, target_role: string | null, question: string) =>
  apiFetch<WhatIfResult>("/students/me/what-if", {
    method: "POST",
    body: JSON.stringify({ company_name, target_role, question }),
  });

// ---- Phase 09: Preparation Plan ----

export interface PreparationReadinessSummary {
  has_analysis: boolean;
  readiness_percentage: number | null;
  status_message: string | null;
}

export interface YearFocus {
  year: string;
  focus_text: string;
  is_current: boolean;
}

export interface Goal {
  id: string;
  text: string;
  completed: boolean;
}

export interface PlanRecommendation {
  title: string;
}

export type GoalKind = "short_term" | "long_term";

export interface PlanRow {
  skill: string;
  category: string;
  filter_category: string;
  current_level: string;
  target_level: string;
  start_date: string;
  end_date: string;
  status: string;
  priority: string;
  resources: string;
}

export interface PreparationPlanPageData {
  target_company: string | null;
  target_role: string | null;
  academic_year: string | null;
  company_options: string[];
  role_options: string[];
  academic_year_options: string[];
  readiness: PreparationReadinessSummary;
  year_wise_focus: YearFocus[];
  short_term_goals: Goal[];
  long_term_goals: Goal[];
  recommendations: PlanRecommendation[];
  has_plan: boolean;
  plan_version: number | null;
  plan_status: string | null;
  plan_items: PlanRow[];
}

export const getPreparationPlanPage = () =>
  apiFetch<PreparationPlanPageData>("/students/me/preparation-plan-page");

export const generatePreparationPlanPage = (
  company_name: string,
  target_role: string | null,
  academic_year: string | null,
) =>
  apiFetch<PreparationPlanPageData>("/students/me/preparation-plan-page/generate", {
    method: "POST",
    body: JSON.stringify({ company_name, target_role, academic_year }),
  });

interface GoalLists {
  short_term_goals: Goal[];
  long_term_goals: Goal[];
}

export const addPreparationGoal = (kind: GoalKind, text: string) =>
  apiFetch<GoalLists>("/students/me/preparation-plan-page/goals", {
    method: "POST",
    body: JSON.stringify({ kind, text }),
  });

export const togglePreparationGoal = (kind: GoalKind, goalId: string) =>
  apiFetch<GoalLists>(
    `/students/me/preparation-plan-page/goals/${encodeURIComponent(goalId)}/toggle?kind=${kind}`,
    { method: "PUT" },
  );

// ---- Phase 10: Student Jobs & Application System ----

export interface FilterOptions {
  companies: string[];
  job_roles: string[];
  locations: string[];
  job_types: string[];
  experience_levels: string[];
}

export interface JobSummary {
  total_jobs: number;
  applied: number;
  under_review: number;
  shortlisted: number;
}

export interface JobCard {
  id: number;
  company_name: string;
  job_title: string;
  job_role: string;
  location: string | null;
  job_type: string | null;
  work_mode: string | null;
  experience_required: string;
  description: string | null;
  required_skills: string[];
  status: string;
  posted_relative: string;
  is_saved: boolean;
  has_applied: boolean;
}

export interface JobsPageData {
  summary: JobSummary;
  filters: FilterOptions;
  jobs: JobCard[];
}

export interface JobFilters {
  search?: string;
  company?: string[];
  job_role?: string[];
  location?: string[];
  job_type?: string[];
  experience_level?: string[];
}

export const getJobsPage = (filters: JobFilters = {}) => {
  const params = new URLSearchParams();
  if (filters.search) params.set("search", filters.search);
  for (const c of filters.company ?? []) params.append("company", c);
  for (const r of filters.job_role ?? []) params.append("job_role", r);
  for (const l of filters.location ?? []) params.append("location", l);
  for (const t of filters.job_type ?? []) params.append("job_type", t);
  for (const e of filters.experience_level ?? []) params.append("experience_level", e);
  const qs = params.toString();
  return apiFetch<JobsPageData>(`/students/me/jobs${qs ? `?${qs}` : ""}`);
};

export const toggleSaveJob = (jobId: number) =>
  apiFetch<{ saved: boolean }>(`/students/me/jobs/${jobId}/save`, { method: "POST" });

export interface MissingRequirement {
  field: string;
  label: string;
  reason: string;
}

export interface ApplyValidation {
  can_apply: boolean;
  missing: MissingRequirement[];
}

export interface Application {
  id: number;
  job_id: number;
  job_title: string;
  company_name: string;
  job_role: string;
  status_label: string;
  disapproval_reason: string | null;
  applied_at: string;
}

export const applyToJob = (jobId: number) =>
  apiFetch<Application>(`/students/me/jobs/${jobId}/apply`, { method: "POST" });

export const getMyApplications = () => apiFetch<Application[]>("/students/me/jobs/applications");

export interface ResumeResult {
  resume_file_path: string | null;
  skills_added: number;
  certifications_added: number;
  projects_added: number;
}

export const getResume = () => apiFetch<ResumeResult>("/students/me/resume");

export async function uploadResume(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiFetch<ResumeResult>("/students/me/resume", {
    method: "POST",
    body: formData,
  });
}

export const deleteResume = () =>
  apiFetch<{ resume_file_path: string | null }>("/students/me/resume", { method: "DELETE" });

// ---- Phase 11: Recruiter Dashboard ----

export interface RecruiterSummary {
  total_jobs: number;
  total_applications: number;
  shortlisted: number;
  under_review: number;
}

export interface RecruiterJobRow {
  id: number;
  job_title: string;
  applications: number;
  shortlisted: number;
  under_review: number;
  rejected: number;
  status: string;
}

export interface PipelineSlice {
  count: number;
  percentage: number;
}

export interface ApplicationPipeline {
  total: number;
  shortlisted: PipelineSlice;
  under_review: PipelineSlice;
  rejected: PipelineSlice;
}

export interface RecentApplicationRow {
  id: number;
  candidate_name: string;
  job_role: string;
  applied_relative: string;
  ai_status: string;
}

export interface UpcomingInterviewRow {
  candidate_name: string;
  job_role: string;
  scheduled_at: string;
  status: string;
}

export interface RecruiterActivityItem {
  label: string;
  detail: string | null;
  relative_time: string;
}

export interface RecruiterDashboardData {
  summary: RecruiterSummary;
  jobs: RecruiterJobRow[];
  pipeline: ApplicationPipeline;
  recent_applications: RecentApplicationRow[];
  upcoming_interviews: UpcomingInterviewRow[];
  recent_activity: RecruiterActivityItem[];
}

export const getRecruiterDashboard = () =>
  apiFetch<RecruiterDashboardData>("/recruiters/me/dashboard");

// ---- Phase 12: Recruiter Job Management ----

export interface RecruiterJobRow {
  id: number;
  company_name: string;
  job_title: string;
  job_role: string;
  experience_required: string;
  location: string | null;
  job_type: string | null;
  work_mode: string | null;
  description: string | null;
  required_skills: string[];
  applications: number;
  shortlisted: number;
  under_review: number;
  rejected: number;
  status: string;
  posted_relative: string;
  created_at: string;
}

export interface RecruiterJobsSummary {
  total_jobs: number;
  active_jobs: number;
  paused_jobs: number;
  total_applications: number;
}

export interface RecruiterJobsPageData {
  summary: RecruiterJobsSummary;
  jobs: RecruiterJobRow[];
}

export const getRecruiterJobsPage = (filters: { search?: string; status?: string } = {}) => {
  const params = new URLSearchParams();
  if (filters.search) params.set("search", filters.search);
  if (filters.status) params.set("status", filters.status);
  const qs = params.toString();
  return apiFetch<RecruiterJobsPageData>(`/recruiters/me/jobs${qs ? `?${qs}` : ""}`);
};

export interface RecruiterJobCreateInput {
  company_name: string;
  job_title: string;
  job_role: string;
  experience_required: string;
  required_skills: string[];
  job_type?: string | null;
  work_mode?: string | null;
  location?: string | null;
  description?: string | null;
}

export const createRecruiterJob = (data: RecruiterJobCreateInput) =>
  apiFetch<RecruiterJobRow>("/recruiters/me/jobs", {
    method: "POST",
    body: JSON.stringify(data),
  });

export const setRecruiterJobStatus = (jobId: number, jobStatus: "active" | "paused") =>
  apiFetch<RecruiterJobRow>(`/recruiters/me/jobs/${jobId}/status`, {
    method: "PUT",
    body: JSON.stringify({ status: jobStatus }),
  });

// ---- Phase 13: Recruiter Candidates Page & Recruitment AI System ----

export interface CandidateSummary {
  total_candidates: number;
  shortlisted: number;
  under_review: number;
  rejected: number;
}

export interface JobOption {
  id: number;
  job_title: string;
}

export interface CandidateFilterOptions {
  jobs: JobOption[];
  statuses: string[];
  ai_evaluations: string[];
}

export interface CandidateRow {
  application_id: number;
  candidate_name: string;
  job_id: number;
  job_title: string;
  applied_role: string;
  applied_relative: string;
  ai_score: number | null;
  matching_factors: string | null;
  status_label: string;
  ai_evaluation_label: string;
}

export interface CandidatesPageData {
  summary: CandidateSummary;
  filters: CandidateFilterOptions;
  candidates: CandidateRow[];
}

export interface CandidateFilters {
  search?: string;
  job_id?: number;
  status?: string;
  ai_evaluation?: string;
}

export const getCandidatesPage = (filters: CandidateFilters = {}) => {
  const params = new URLSearchParams();
  if (filters.search) params.set("search", filters.search);
  if (filters.job_id !== undefined) params.set("job_id", String(filters.job_id));
  if (filters.status) params.set("status", filters.status);
  if (filters.ai_evaluation) params.set("ai_evaluation", filters.ai_evaluation);
  const qs = params.toString();
  return apiFetch<CandidatesPageData>(`/recruiters/me/candidates${qs ? `?${qs}` : ""}`);
};

export type WorkflowStageState =
  "pending" | "running" | "completed" | "failed" | "paused" | "approved" | "rejected";

export interface WorkflowStage {
  key: string;
  label: string;
  state: WorkflowStageState;
}

export interface SelectedCandidate {
  candidate_name: string;
  applied_role: string;
  ai_score: number | null;
}

export interface CandidateWorkflow {
  selected_candidate: SelectedCandidate;
  stages: WorkflowStage[];
  matching_factors: string | null;
  matched_skills: string[];
  missing_skills: string[];
  human_decision: "approved" | "disapproved" | null;
  disapproval_reason: string | null;
  historical_signal: string | null;
  interview_question_count: number;
  email_status: "pending" | "sending" | "sent" | "failed" | null;
  email_status_label: string | null;
  recipient_email: string | null;
  email_source: "profile" | "resume" | "unavailable" | null;
  email_error: string | null;
}

export const getCandidateWorkflow = (applicationId: number) =>
  apiFetch<CandidateWorkflow>(`/recruiters/me/candidates/${applicationId}/workflow`);

// ---- Phase 14: Human Approval & Recruitment Outcome ----

export const approveCandidate = (applicationId: number) =>
  apiFetch<CandidateWorkflow>(`/recruiters/me/candidates/${applicationId}/approve`, {
    method: "POST",
  });

export const disapproveCandidate = (applicationId: number, reason: string) =>
  apiFetch<CandidateWorkflow>(`/recruiters/me/candidates/${applicationId}/disapprove`, {
    method: "POST",
    body: JSON.stringify({ reason }),
  });

// ---- Phase 15: Interview Agent, Interviews Page & Email Agent ----

export interface InterviewSummary {
  total_interviews: number;
  scheduled: number;
  completed: number;
  cancelled: number;
}

export interface InterviewFilterOptions {
  jobs: JobOption[];
  statuses: string[];
}

export interface InterviewRow {
  application_id: number;
  candidate_name: string;
  job_id: number;
  job_role: string;
  interview_type: string | null;
  scheduled_at: string | null;
  scheduled_at_display: string | null;
  ai_status_label: string;
  status_label: string;
  outcome_label: string | null;
}

export interface EligibleCandidate {
  application_id: number;
  candidate_name: string;
  job_role: string;
}

export interface InterviewsPageData {
  summary: InterviewSummary;
  filters: InterviewFilterOptions;
  interviews: InterviewRow[];
  eligible_candidates: EligibleCandidate[];
  recent_activity: RecentActivityItem[];
}

export const getInterviewsPage = () => apiFetch<InterviewsPageData>("/recruiters/me/interviews");

export interface InterviewQuestion {
  question_text: string;
  category: string | null;
  evaluation_criteria: string | null;
}

export interface InterviewDetail {
  candidate_name: string;
  job_role: string;
  interview_type: string | null;
  scheduled_at_display: string | null;
  ai_status_label: string;
  status_label: string;
  questions: InterviewQuestion[];
  invitation_subject: string | null;
  invitation_body: string | null;
  missing_skills: string[];
  outcome: "hired" | "not_selected" | null;
  outcome_label: string | null;
  outcome_reason: string | null;
  email_status: "pending" | "sending" | "sent" | "failed";
  email_status_label: string;
  recipient_email: string | null;
  email_source: "profile" | "resume" | "unavailable" | null;
  email_sent_at_display: string | null;
  email_error: string | null;
}

export const getInterviewDetail = (applicationId: number) =>
  apiFetch<InterviewDetail>(`/recruiters/me/interviews/${applicationId}`);

export const scheduleInterview = (
  applicationId: number,
  interviewType: string,
  scheduledAt: string,
) =>
  apiFetch<InterviewDetail>(`/recruiters/me/interviews/${applicationId}/schedule`, {
    method: "POST",
    body: JSON.stringify({ interview_type: interviewType, scheduled_at: scheduledAt }),
  });

export const setInterviewStatus = (
  applicationId: number,
  status: "scheduled" | "completed" | "cancelled",
) =>
  apiFetch<InterviewDetail>(`/recruiters/me/interviews/${applicationId}/status`, {
    method: "PUT",
    body: JSON.stringify({ status }),
  });

// ---- Phase 16: Student Application Outcome & Closed-Loop Intelligence ----

export const setInterviewOutcome = (
  applicationId: number,
  outcome: "hired" | "not_selected",
  reason?: string,
) =>
  apiFetch<InterviewDetail>(`/recruiters/me/interviews/${applicationId}/outcome`, {
    method: "PUT",
    body: JSON.stringify({ outcome, reason }),
  });

// ---- Phase 17: Recruitment Analytics & Historical Intelligence ----

export interface FunnelStage {
  label: string;
  count: number;
}

export interface OutcomeSlice {
  label: string;
  count: number;
}

export interface SkillTrend {
  skill: string;
  count: number;
}

export interface StageTrendPoint {
  period: string;
  applications: number;
}

export interface CompanyPattern {
  job_id: number;
  job_title: string;
  job_role: string;
  applications: number;
  hire_rate_percentage: number;
  average_ai_score: number | null;
}

export interface SuccessfulCandidateProfile {
  total_hired: number;
  average_ai_score: number | null;
  top_skills: string[];
}

export interface RecruiterAnalyticsData {
  funnel: FunnelStage[];
  outcomes: OutcomeSlice[];
  skill_trends: SkillTrend[];
  skill_gap_trends: SkillTrend[];
  stage_trends: StageTrendPoint[];
  company_patterns: CompanyPattern[];
  successful_candidate_profile: SuccessfulCandidateProfile;
}

export const getRecruiterAnalytics = () =>
  apiFetch<RecruiterAnalyticsData>("/recruiters/me/analytics");

// ---- Phase 18: My Profile / Student Progress ----

export interface ProfileOverview {
  full_name: string | null;
  degree: string | null;
  college: string | null;
  current_semester: string | null;
  city: string | null;
  state: string | null;
  profile_photo_path: string | null;
  has_resume: boolean;
}

export interface ProfileStats {
  skills_added: number;
  projects: number;
  certifications: number;
  job_applications: number;
}

export interface MissingField {
  section: string;
  field: string;
}

export interface ProfilePageData {
  overview: ProfileOverview;
  completion_percentage: number;
  missing_fields: MissingField[];
  stats: ProfileStats;
}

export const getProfilePage = () => apiFetch<ProfilePageData>("/students/me/profile");

export interface CareerPlacement {
  career_interest: string | null;
  target_job_role: string | null;
  preferred_job_domain: string | null;
  target_company: string | null;
  target_role: string | null;
  preferred_technology_skill_area: string[];
  placement_interest: string | null;
  internship_interest: string | null;
  preferred_job_type: string | null;
  preferred_work_location: string | null;
  preferred_country: string | null;
  preferred_state: string | null;
  preferred_city: string | null;
  remote_onsite_hybrid: string | null;
  preferred_industry: string | null;
  placement_status: string | null;
}

export const getCareerPlacement = () =>
  apiFetch<CareerPlacement | null>("/students/me/career-placement");
export const putCareerPlacement = (data: CareerPlacement) =>
  apiFetch<CareerPlacement>("/students/me/career-placement", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export interface LearningPreparation {
  current_learning_areas: string[];
  skills_currently_learning: string[];
  learning_goals: string[];
  areas_to_improve: string[];
  current_preparation_status: string | null;
  previous_interview_experience: string | null;
  previous_assessment_experience: string | null;
  technical_interview_experience: string | null;
  coding_assessment_experience: string | null;
  interview_preparation_status: string | null;
  assessment_preparation_status: string | null;
}

export const getLearningPreparation = () =>
  apiFetch<LearningPreparation | null>("/students/me/learning-preparation");
export const putLearningPreparation = (data: LearningPreparation) =>
  apiFetch<LearningPreparation>("/students/me/learning-preparation", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export interface ProfessionalLinks {
  github_url: string | null;
  linkedin_url: string | null;
  portfolio_website_url: string | null;
  coding_profile_url: string | null;
  other_professional_profile_url: string | null;
  resume_file_path: string | null;
}

export const getProfessionalLinks = () =>
  apiFetch<ProfessionalLinks | null>("/students/me/professional-links");
export const putProfessionalLinks = (data: Omit<ProfessionalLinks, "resume_file_path">) =>
  apiFetch<ProfessionalLinks>("/students/me/professional-links", {
    method: "PUT",
    body: JSON.stringify(data),
  });

export interface Consent {
  consent_use_information: boolean;
  consent_learning_experience: boolean;
  consent_anonymized_intelligence: boolean;
}

export const getConsent = () => apiFetch<Consent | null>("/students/me/consent");
export const putConsent = (data: Consent) =>
  apiFetch<Consent>("/students/me/consent", { method: "PUT", body: JSON.stringify(data) });

export interface RecruitmentApplicationRow {
  company_name: string;
  job_role: string;
  applied_relative: string;
  recruitment_stage_reached: string;
  outcome: string | null;
}

export interface RecruitmentHistory {
  total_applications: number;
  companies_applied_to: string[];
  roles_applied_to: string[];
  selected_count: number;
  rejected_count: number;
  hold_count: number;
  applications: RecruitmentApplicationRow[];
}

export const getRecruitmentHistory = () =>
  apiFetch<RecruitmentHistory>("/students/me/recruitment-history");

export const deleteAccount = () =>
  apiFetch<{ deleted: boolean }>("/students/me/account", { method: "DELETE" });
