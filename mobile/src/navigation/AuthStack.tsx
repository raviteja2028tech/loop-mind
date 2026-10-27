import { createNativeStackNavigator } from "@react-navigation/native-stack";
import WelcomeScreen from "@/screens/auth/WelcomeScreen";
import OtpScreen from "@/screens/auth/OtpScreen";

export type AuthStackParamList = {
  Welcome: undefined;
  Otp: { mobileNumber: string; purpose: "login" | "register" };
};

const Stack = createNativeStackNavigator<AuthStackParamList>();

/** Mirrors the web's Login/Create Account + Enter OTP modal chain
 * (phase.md Phase 03), as full screens instead of modals — the native
 * equivalent of the same flow, same backend endpoints. */
export default function AuthStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Welcome" component={WelcomeScreen} />
      <Stack.Screen name="Otp" component={OtpScreen} />
    </Stack.Navigator>
  );
}
