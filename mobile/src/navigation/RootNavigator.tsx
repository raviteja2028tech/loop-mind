import * as React from "react";
import { NavigationContainer, DarkTheme } from "@react-navigation/native";
import { ActivityIndicator, View } from "react-native";
import { colors } from "@/lib/theme";
import { useAuth } from "@/lib/auth";
import AuthStack from "./AuthStack";
import StudentTabs from "./StudentTabs";
import RecruiterTabs from "./RecruiterTabs";

const navTheme = {
  ...DarkTheme,
  colors: {
    ...DarkTheme.colors,
    background: colors.bg,
    card: colors.bg,
    text: colors.text,
    border: colors.border,
    primary: colors.accent,
  },
};

export default function RootNavigator() {
  const { token, role, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg }}>
        <ActivityIndicator color={colors.accent} />
      </View>
    );
  }

  return (
    <NavigationContainer theme={navTheme}>
      {!token ? <AuthStack /> : role === "recruiter" ? <RecruiterTabs /> : <StudentTabs />}
    </NavigationContainer>
  );
}
