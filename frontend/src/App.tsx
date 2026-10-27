import { BrowserRouter, Route, Routes } from "react-router-dom";
import JobsPage from "@/app/JobsPage";
import MyProfilePage, { PublicProfileView } from "@/app/MyProfilePage";
import PreparationPlanPage from "@/app/PreparationPlanPage";
import SkillGapAnalysis from "@/app/SkillGapAnalysis";
import StudentDashboard from "@/app/StudentDashboard";
import { AuthModalProvider, InfoModalsProvider } from "@/components";
import { AuthProvider, RequireRole } from "@/lib/auth";
import AnalyticsPage from "@/recruiter/AnalyticsPage";
import CandidatesPage from "@/recruiter/CandidatesPage";
import InterviewsPage from "@/recruiter/InterviewsPage";
import JobManagementPage from "@/recruiter/JobManagementPage";
import RecruiterDashboard from "@/recruiter/RecruiterDashboard";
import LandingPage from "@/website/LandingPage";
import LinkedInOAuthCallback from "@/website/LinkedInOAuthCallback";
import { OnboardingModalProvider } from "@/website/onboarding/OnboardingModalProvider";

/**
 * Root route tree.
 *
 * Phase 02 added the public Landing Page. Phase 03 added authentication
 * (Login/Create Account/OTP + JWT) and role-based routing to /app
 * (student) and /recruiter (recruiter). Phase 05 continues a successful
 * *registration* as an onboarding modal chain still on "/" (spec.md: not
 * a separate page) before eventually landing on /app — see the portal
 * placeholder components for what still belongs to later phases.
 */
function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <InfoModalsProvider>
          <OnboardingModalProvider>
            <AuthModalProvider>
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/linkedin/oauth-callback" element={<LinkedInOAuthCallback />} />
                <Route
                  path="/app"
                  element={
                    <RequireRole role="student">
                      <StudentDashboard />
                    </RequireRole>
                  }
                />
                <Route
                  path="/app/skill-gap"
                  element={
                    <RequireRole role="student">
                      <SkillGapAnalysis />
                    </RequireRole>
                  }
                />
                <Route
                  path="/app/preparation-plan"
                  element={
                    <RequireRole role="student">
                      <PreparationPlanPage />
                    </RequireRole>
                  }
                />
                <Route
                  path="/app/jobs"
                  element={
                    <RequireRole role="student">
                      <JobsPage />
                    </RequireRole>
                  }
                />
                <Route
                  path="/app/profile"
                  element={
                    <RequireRole role="student">
                      <MyProfilePage />
                    </RequireRole>
                  }
                />
                <Route
                  path="/app/profile/public"
                  element={
                    <RequireRole role="student">
                      <PublicProfileView />
                    </RequireRole>
                  }
                />
                <Route
                  path="/recruiter"
                  element={
                    <RequireRole role="recruiter">
                      <RecruiterDashboard />
                    </RequireRole>
                  }
                />
                <Route
                  path="/recruiter/jobs"
                  element={
                    <RequireRole role="recruiter">
                      <JobManagementPage />
                    </RequireRole>
                  }
                />
                <Route
                  path="/recruiter/candidates"
                  element={
                    <RequireRole role="recruiter">
                      <CandidatesPage />
                    </RequireRole>
                  }
                />
                <Route
                  path="/recruiter/interviews"
                  element={
                    <RequireRole role="recruiter">
                      <InterviewsPage />
                    </RequireRole>
                  }
                />
                <Route
                  path="/recruiter/analytics"
                  element={
                    <RequireRole role="recruiter">
                      <AnalyticsPage />
                    </RequireRole>
                  }
                />
              </Routes>
            </AuthModalProvider>
          </OnboardingModalProvider>
        </InfoModalsProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
