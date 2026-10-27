import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { colors } from "@/lib/theme";
import RecruiterDashboardScreen from "@/screens/recruiter/DashboardScreen";
import RecruiterJobsScreen from "@/screens/recruiter/JobsScreen";
import RecruiterCandidatesScreen from "@/screens/recruiter/CandidatesScreen";

const Tab = createBottomTabNavigator();

/** phase.md Phase 19: "recruiter workflows where the mobile scope defines
 * them" — spec.md never defines a mobile Recruiter Portal reference layout
 * the way it does for Student Portal pages, so this is deliberately the
 * minimal, honest set: read the same Dashboard/Jobs/Candidates data the
 * web Recruiter Portal shows, plus the one action explicit everywhere
 * else in the spec (Approve). No AI workflow visualization (React Flow
 * has no mobile-native equivalent) and no Interviews/Analytics screens —
 * inventing those here would be exactly the "mobile-only product feature"
 * phase.md's critical architecture rule forbids. */
export default function RecruiterTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: colors.bg },
        headerTintColor: colors.text,
        tabBarStyle: { backgroundColor: colors.chrome, borderTopColor: colors.border },
        tabBarActiveTintColor: colors.accent,
        tabBarInactiveTintColor: colors.textMute,
      }}
    >
      <Tab.Screen name="Dashboard" component={RecruiterDashboardScreen} />
      <Tab.Screen name="Jobs" component={RecruiterJobsScreen} />
      <Tab.Screen name="Candidates" component={RecruiterCandidatesScreen} />
    </Tab.Navigator>
  );
}
