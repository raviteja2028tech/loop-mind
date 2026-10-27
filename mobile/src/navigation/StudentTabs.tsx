import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { colors } from "@/lib/theme";
import DashboardScreen from "@/screens/student/DashboardScreen";
import SkillGapScreen from "@/screens/student/SkillGapScreen";
import PreparationPlanScreen from "@/screens/student/PreparationPlanScreen";
import JobsScreen from "@/screens/student/JobsScreen";
import ProfileScreen from "@/screens/student/ProfileScreen";

const Tab = createBottomTabNavigator();

/** phase.md Phase 19 "Required mobile behavior": student dashboard, Skill
 * Gap, Preparation Plan, Jobs/applications, student profile — the same
 * five destinations as the web navbar (Dashboard | Skill Gap |
 * Preparation Plan | Jobs | My Profile), as bottom tabs instead of a top
 * nav bar (the native convention), same backend data either way. */
export default function StudentTabs() {
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
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Skill Gap" component={SkillGapScreen} />
      <Tab.Screen name="Prep Plan" component={PreparationPlanScreen} />
      <Tab.Screen name="Jobs" component={JobsScreen} />
      <Tab.Screen name="My Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
