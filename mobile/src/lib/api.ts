/**
 * REST client for the LOOP-MIND FastAPI backend — phase.md Phase 19
 * "Critical architecture rule": the mobile app calls the exact same
 * backend/API as the web app (frontend/src/lib/api.ts), never a second
 * backend or duplicated business logic. Shapes here mirror that file's
 * types for the endpoints this app actually uses.
 *
 * React Native has no dev proxy like Vite's, so the base URL is explicit.
 * `localhost` resolves to the phone/emulator itself, not your computer —
 * set EXPO_PUBLIC_API_BASE_URL to your machine's LAN IP (e.g.
 * "http://192.168.1.20:8010/api") when running on a physical device or
 * Android emulator; the Android emulator's own loopback alias is
 * 10.0.2.2 instead of localhost.
 */
import AsyncStorage from "@react-native-async-storage/async-storage";

const DEFAULT_BASE_URL = "http://localhost:8010/api";
export const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL ?? DEFAULT_BASE_URL;

const AUTH_TOKEN_KEY = "loop-mind.auth-token";

export async function getAuthToken(): Promise<string | null> {
  try {
    return await AsyncStorage.getItem(AUTH_TOKEN_KEY);
  } catch {
    return null;
  }
}

export async function setAuthToken(token: string | null): Promise<void> {
  try {
    if (token) await AsyncStorage.setItem(AUTH_TOKEN_KEY, token);
    else await AsyncStorage.removeItem(AUTH_TOKEN_KEY);
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

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = await getAuthToken();
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body) headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });
  const contentType = res.headers.get("content-type") ?? "";
  const data = contentType.includes("application/json")
    ? await res.json().catch(() => null)
    : await res.text();

  if (!res.ok) throw new ApiError(res.status, data);
  return data as T;
}

// ---- Auth (phase.md Phase 03) ----

export type Purpose = "login" | "register";
export type Role = "student" | "recruiter";

export interface SendOtpResponse {
  mobile_number: string;
  resend_available_in_seconds: number;
  dev_otp?: string | null;
}

export interface AuthSuccessResponse {
  token: string;
  role: Role;
  redirect: string;
}

export const sendOtp = (mobileNumber: string, purpose: Purpose) =>
  apiFetch<SendOtpResponse>("/auth/send-otp", {
    method: "POST",
    body: JSON.stringify({ mobile_number: mobileNumber, purpose }),
  });

export const verifyOtp = (mobileNumber: string, code: string, purpose: Purpose) =>
  apiFetch<AuthSuccessResponse>("/auth/verify-otp", {
    method: "POST",
    body: JSON.stringify({ mobile_number: mobileNumber, code, purpose }),
  });

export interface MeResponse {
  id: number;
  mobile_number: string;
  role: Role;
}

export const getMe = () => apiFetch<MeResponse>("/auth/me");

// ---- Student Dashboard (phase.md Phase 07) ----

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

export interface DashboardData {
  full_name: string;
  profile_completion_percentage: number;
  skills_count: number;
  projects_count: number;
  certifications_count: number;
  target_company: string | null;
  placement_readiness: PlacementReadinessSummary;
  recent_activity: RecentActivityItem[];
}

export const getDashboard = () => apiFetch<DashboardData>("/students/me/dashboard");

// ---- Skill Gap Analysis (phase.md Phase 08) ----

export interface ReadinessOut {
  has_analysis: boolean;
  readiness_percentage: number | null;
  status_message: string | null;
  supporting_text: string | null;
}

export interface SkillRowOut {
  skill: string;
  category: string;
  your_level: string;
  required_level: string;
  status: string;
  priority: string | null;
  resources: string | null;
}

export interface SkillGapPageOut {
  target_company: string | null;
  target_role: string | null;
  readiness: ReadinessOut;
  overview: {
    total_required_skills: number;
    skills_you_have: number;
    skills_to_improve: number;
    missing_evidence: number;
  };
  priority_areas: { rank: number; skill: string; impact: string }[];
  skills: SkillRowOut[];
}

export const getSkillGapPage = () => apiFetch<SkillGapPageOut>("/students/me/skill-gap");

// ---- Preparation Plan (phase.md Phase 09) ----

export interface Goal {
  id: string;
  text: string;
  completed: boolean;
}

export interface YearFocus {
  year: string;
  focus_text: string;
  is_current: boolean;
}

export interface PreparationPlanPageOut {
  target_company: string | null;
  target_role: string | null;
  readiness: ReadinessOut;
  year_wise_focus: YearFocus[];
  short_term_goals: Goal[];
  long_term_goals: Goal[];
}

export const getPreparationPlanPage = () =>
  apiFetch<PreparationPlanPageOut>("/students/me/preparation-plan-page");

export const toggleGoal = (goalId: string) =>
  apiFetch<{ short_term_goals: Goal[]; long_term_goals: Goal[] }>(
    `/students/me/preparation-plan-page/goals/${goalId}/toggle`,
    { method: "PUT" },
  );

// ---- Jobs & Applications (phase.md Phase 10) ----

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

export interface JobSummary {
  total_jobs: number;
  applied: number;
  under_review: number;
  shortlisted: number;
}

export interface JobsPageOut {
  summary: JobSummary;
  jobs: JobCard[];
}

export const getJobsPage = () => apiFetch<JobsPageOut>("/students/me/jobs");

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

export const toggleSaveJob = (jobId: number) =>
  apiFetch<{ saved: boolean }>(`/students/me/jobs/${jobId}/save`, { method: "POST" });

export const getMyApplications = () => apiFetch<Application[]>("/students/me/jobs/applications");

// ---- My Profile (phase.md Phase 18) ----

export interface ProfileOverview {
  full_name: string | null;
  degree: string | null;
  college: string | null;
  current_semester: string | null;
  city: string | null;
  state: string | null;
  profile_photo_path: string | null;
}

export interface ProfileStats {
  skills_added: number;
  projects: number;
  certifications: number;
  job_applications: number;
}

export interface ProfilePageData {
  overview: ProfileOverview;
  completion_percentage: number;
  missing_fields: { section: string; field: string }[];
  stats: ProfileStats;
}

export const getProfilePage = () => apiFetch<ProfilePageData>("/students/me/profile");

export interface StudentSkill {
  id: number;
  skill_name: string;
  skill_category: string;
  proficiency: string;
  learning_status: string;
  experience_years: number | null;
}

export const listSkills = () => apiFetch<StudentSkill[]>("/students/me/skills");

export interface RecruitmentApplicationRow {
  company_name: string;
  job_role: string;
  applied_relative: string;
  recruitment_stage_reached: string;
  outcome: string | null;
}

export interface RecruitmentHistory {
  total_applications: number;
  selected_count: number;
  rejected_count: number;
  hold_count: number;
  applications: RecruitmentApplicationRow[];
}

export const getRecruitmentHistory = () =>
  apiFetch<RecruitmentHistory>("/students/me/recruitment-history");

// ---- Recruiter Dashboard (phase.md Phase 11) ----

export interface RecruiterSummary {
  total_jobs: number;
  total_applications: number;
  shortlisted: number;
  under_review: number;
  rejected: number;
}

export interface RecruiterDashboardData {
  summary: RecruiterSummary;
  recent_activity: RecentActivityItem[];
}

export const getRecruiterDashboard = () => apiFetch<RecruiterDashboardData>("/recruiters/me/dashboard");

// ---- Recruiter Jobs (phase.md Phase 12) ----

export interface RecruiterJobRow {
  id: number;
  job_title: string;
  job_role: string;
  experience_required: string;
  applications: number;
  shortlisted: number;
  under_review: number;
  rejected: number;
  status: string;
  posted_relative: string;
}

export const getRecruiterJobsPage = () =>
  apiFetch<{ jobs: RecruiterJobRow[] }>("/recruiters/me/jobs");

// ---- Recruiter Candidates (phase.md Phase 13-14) ----

export interface CandidateRow {
  application_id: number;
  candidate_name: string;
  job_title: string;
  applied_role: string;
  applied_relative: string;
  ai_score: number | null;
  status_label: string;
  ai_evaluation_label: string;
}

export const getCandidatesPage = () =>
  apiFetch<{ candidates: CandidateRow[] }>("/recruiters/me/candidates");

export const approveCandidate = (applicationId: number) =>
  apiFetch<unknown>(`/recruiters/me/candidates/${applicationId}/approve`, { method: "POST" });
