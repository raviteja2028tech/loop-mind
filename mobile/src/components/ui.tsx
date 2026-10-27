/**
 * Minimal native translation of the web's Graphite Ink component
 * primitives (frontend/src/components/*) — phase.md Phase 19 "Mobile
 * visual rule": same palette/typography/card language, native widgets
 * instead of CSS since React Native has no stylesheet cascade.
 */
import * as React from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
  type StyleProp,
  type ViewStyle,
} from "react-native";
import { colors, fontSizes, radius, spacing } from "@/lib/theme";

export function Screen({ children }: { children: React.ReactNode }) {
  return <View style={styles.screen}>{children}</View>;
}

export function Card({
  children,
  style,
}: {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
}) {
  return <View style={[styles.card, style]}>{children}</View>;
}

export function H2({ children }: { children: React.ReactNode }) {
  return <Text style={styles.h2}>{children}</Text>;
}

export function H3({ children }: { children: React.ReactNode }) {
  return <Text style={styles.h3}>{children}</Text>;
}

export function Muted({ children }: { children: React.ReactNode }) {
  return <Text style={styles.muted}>{children}</Text>;
}

export function BodyText({ children }: { children: React.ReactNode }) {
  return <Text style={styles.body}>{children}</Text>;
}

type ButtonVariant = "primary" | "ghost" | "danger";

export function Button({
  title,
  onPress,
  variant = "primary",
  disabled,
  loading,
}: {
  title: string;
  onPress: () => void;
  variant?: ButtonVariant;
  disabled?: boolean;
  loading?: boolean;
}) {
  const isDisabled = disabled || loading;
  return (
    <Pressable
      onPress={onPress}
      disabled={isDisabled}
      style={({ pressed }) => [
        styles.button,
        variant === "ghost" && styles.buttonGhost,
        variant === "danger" && styles.buttonDanger,
        isDisabled && styles.buttonDisabled,
        pressed && !isDisabled && { opacity: 0.85 },
      ]}
    >
      {loading ? (
        <ActivityIndicator color={variant === "ghost" ? colors.text : colors.bg} />
      ) : (
        <Text
          style={[
            styles.buttonText,
            variant === "ghost" && styles.buttonTextGhost,
            variant === "danger" && styles.buttonTextDanger,
          ]}
        >
          {title}
        </Text>
      )}
    </Pressable>
  );
}

export function TextField({
  value,
  onChangeText,
  placeholder,
  keyboardType,
  maxLength,
  secureTextEntry,
  editable = true,
  autoCapitalize = "none",
}: {
  value: string;
  onChangeText: (v: string) => void;
  placeholder?: string;
  keyboardType?: "default" | "numeric" | "email-address" | "phone-pad";
  maxLength?: number;
  secureTextEntry?: boolean;
  editable?: boolean;
  autoCapitalize?: "none" | "sentences" | "words" | "characters";
}) {
  return (
    <TextInput
      value={value}
      onChangeText={onChangeText}
      placeholder={placeholder}
      placeholderTextColor={colors.textMute}
      keyboardType={keyboardType}
      maxLength={maxLength}
      secureTextEntry={secureTextEntry}
      editable={editable}
      autoCapitalize={autoCapitalize}
      style={[styles.input, !editable && { opacity: 0.6 }]}
    />
  );
}

export function Badge({
  label,
  tone = "neutral",
}: {
  label: string;
  tone?: "ok" | "hold" | "rejected" | "neutral";
}) {
  const toneStyle = {
    ok: { background: colors.accentWash, color: colors.accent },
    hold: { background: colors.warnWash, color: colors.warn },
    rejected: { background: colors.dangerWash, color: colors.danger },
    neutral: { background: colors.raised, color: colors.textMute },
  }[tone];
  return (
    <View style={[styles.badge, { backgroundColor: toneStyle.background }]}>
      <Text style={[styles.badgeText, { color: toneStyle.color }]}>{label}</Text>
    </View>
  );
}

export function StatBlock({ label, value, accent }: { label: string; value: string | number; accent?: boolean }) {
  return (
    <Card style={styles.statBlock}>
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={[styles.statValue, accent && { color: colors.accent }]}>{value}</Text>
    </Card>
  );
}

export function LoadingBlock({ label }: { label: string }) {
  return (
    <View style={styles.centerBlock}>
      <ActivityIndicator color={colors.accent} />
      <Muted>{label}</Muted>
    </View>
  );
}

export function ErrorBlock({ message }: { message: string }) {
  return (
    <View style={[styles.centerBlock, { backgroundColor: colors.dangerWash, borderRadius: radius.sm }]}>
      <Text style={{ color: colors.danger }}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg,
  },
  card: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.lg,
    padding: spacing.lg,
    gap: spacing.sm,
  },
  h2: {
    color: colors.text,
    fontSize: fontSizes.xl,
    fontWeight: "600",
  },
  h3: {
    color: colors.text,
    fontSize: fontSizes.lg,
    fontWeight: "600",
  },
  muted: {
    color: colors.textMute,
    fontSize: fontSizes.sm,
  },
  body: {
    color: colors.textSoft,
    fontSize: fontSizes.base,
  },
  button: {
    backgroundColor: colors.accent,
    borderRadius: radius.sm,
    paddingVertical: 12,
    paddingHorizontal: 18,
    alignItems: "center",
    justifyContent: "center",
  },
  buttonGhost: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: colors.borderHi,
  },
  buttonDanger: {
    backgroundColor: colors.danger,
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: colors.bg,
    fontWeight: "600",
    fontSize: fontSizes.base,
  },
  buttonTextGhost: {
    color: colors.text,
  },
  buttonTextDanger: {
    color: colors.bg,
  },
  input: {
    backgroundColor: colors.raised,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.sm,
    paddingHorizontal: 14,
    paddingVertical: 10,
    color: colors.text,
    fontSize: fontSizes.base,
  },
  badge: {
    alignSelf: "flex-start",
    borderRadius: 999,
    paddingVertical: 4,
    paddingHorizontal: 10,
  },
  badgeText: {
    fontSize: fontSizes.xs,
    fontWeight: "600",
  },
  statBlock: {
    flex: 1,
    alignItems: "flex-start",
  },
  statLabel: {
    color: colors.textMute,
    fontSize: fontSizes.xs,
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },
  statValue: {
    color: colors.text,
    fontSize: fontSizes.xxl,
    fontWeight: "700",
  },
  centerBlock: {
    padding: spacing.lg,
    alignItems: "center",
    gap: spacing.sm,
  },
});
