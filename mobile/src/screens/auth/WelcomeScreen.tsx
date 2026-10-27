import * as React from "react";
import { KeyboardAvoidingView, Platform, StyleSheet, View } from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import { Button, H2, H3, Muted, Screen, TextField } from "@/components/ui";
import { ApiError, sendOtp, type Purpose } from "@/lib/api";
import { spacing } from "@/lib/theme";
import type { AuthStackParamList } from "@/navigation/AuthStack";

type Props = NativeStackScreenProps<AuthStackParamList, "Welcome">;

/** Mobile number entry for both Login and Create Account — phase.md
 * Phase 19 reproduces this behavior from frontend/src/components/
 * AuthModalProvider.tsx's "mobile" step, same two backend purposes
 * ("login" | "register"), same validation (exactly 10 digits),
 * same account-existence error mapping. */
export default function WelcomeScreen({ navigation }: Props) {
  const [purpose, setPurpose] = React.useState<Purpose>("login");
  const [mobile, setMobile] = React.useState("");
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);

  const mobileValid = /^\d{10}$/.test(mobile);

  async function handleSubmit() {
    if (!mobileValid) return;
    setError(null);
    setLoading(true);
    try {
      await sendOtp(mobile, purpose);
      navigation.navigate("Otp", { mobileNumber: mobile, purpose });
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setError("No account exists with this mobile number. Try Create Account instead.");
      } else if (err instanceof ApiError && err.status === 409) {
        setError("An account already exists with this mobile number. Try Login instead.");
      } else if (err instanceof ApiError && err.status === 429) {
        setError("Please wait a moment before requesting another code.");
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <Screen>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <View style={styles.container}>
          <H2>LOOP-MIND</H2>
          <Muted>AI Recruitment Agent & Closed-Loop Campus Recruitment Intelligence</Muted>

          <View style={styles.tabs}>
            <Button
              title="Login"
              variant={purpose === "login" ? "primary" : "ghost"}
              onPress={() => {
                setPurpose("login");
                setError(null);
              }}
            />
            <Button
              title="Create Account"
              variant={purpose === "register" ? "primary" : "ghost"}
              onPress={() => {
                setPurpose("register");
                setError(null);
              }}
            />
          </View>

          <View style={styles.field}>
            <H3>Mobile Number</H3>
            <TextField
              value={mobile}
              onChangeText={(v) => setMobile(v.replace(/\D/g, "").slice(0, 10))}
              placeholder="10-digit mobile number"
              keyboardType="phone-pad"
              maxLength={10}
            />
          </View>

          {error ? <Muted>{error}</Muted> : null}

          <Button
            title={purpose === "login" ? "Send OTP to Login" : "Send OTP to Create Account"}
            onPress={handleSubmit}
            disabled={!mobileValid}
            loading={loading}
          />

          <Muted>Demo OTP is always 1111 in this environment.</Muted>
        </View>
      </KeyboardAvoidingView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    paddingHorizontal: spacing.xl,
    gap: spacing.md,
  },
  tabs: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  field: {
    gap: spacing.xs,
  },
});
