import * as React from "react";
import { StyleSheet, View } from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import { Button, H2, H3, Muted, Screen, TextField } from "@/components/ui";
import { ApiError, sendOtp, verifyOtp } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { spacing } from "@/lib/theme";
import type { AuthStackParamList } from "@/navigation/AuthStack";

type Props = NativeStackScreenProps<AuthStackParamList, "Otp">;

const RESEND_COOLDOWN_SECONDS = 30;

/** Same OTP mechanics as frontend/src/components/AuthModalProvider.tsx's
 * "otp" step and the same backend `/auth/verify-otp` — a 4-digit code,
 * fixed at 1111 in this dev environment (backend/core/security.py's
 * DEV_OTP_CODE), with a resend cooldown. */
export default function OtpScreen({ route }: Props) {
  const { mobileNumber, purpose } = route.params;
  const { login } = useAuth();

  const [code, setCode] = React.useState("");
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [resendIn, setResendIn] = React.useState(RESEND_COOLDOWN_SECONDS);

  React.useEffect(() => {
    if (resendIn <= 0) return;
    const id = setInterval(() => setResendIn((s) => Math.max(0, s - 1)), 1000);
    return () => clearInterval(id);
  }, [resendIn]);

  async function handleVerify() {
    if (code.length !== 4) return;
    setError(null);
    setLoading(true);
    try {
      const result = await verifyOtp(mobileNumber, code, purpose);
      await login(result.token, result.role);
    } catch (err) {
      if (err instanceof ApiError && err.status === 400) {
        setError("Incorrect OTP, please try again.");
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleResend() {
    setError(null);
    try {
      await sendOtp(mobileNumber, purpose);
      setResendIn(RESEND_COOLDOWN_SECONDS);
    } catch {
      setError("Could not resend the code. Please try again.");
    }
  }

  return (
    <Screen>
      <View style={styles.container}>
        <H2>Enter OTP</H2>
        <Muted>We sent a 4-digit code to {mobileNumber}.</Muted>

        <View style={styles.field}>
          <H3>OTP Code</H3>
          <TextField
            value={code}
            onChangeText={(v) => setCode(v.replace(/\D/g, "").slice(0, 4))}
            placeholder="1111"
            keyboardType="numeric"
            maxLength={4}
          />
        </View>

        {error ? <Muted>{error}</Muted> : null}

        <Button title="Verify & Continue" onPress={handleVerify} disabled={code.length !== 4} loading={loading} />

        <Button
          title={resendIn > 0 ? `Resend code in ${resendIn}s` : "Resend code"}
          variant="ghost"
          onPress={handleResend}
          disabled={resendIn > 0}
        />
      </View>
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
  field: {
    gap: spacing.xs,
  },
});
