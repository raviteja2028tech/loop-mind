/**
 * LOOP-MIND Graphite Ink palette — ported verbatim from
 * frontend/src/styles/agenthire-theme.css. phase.md Phase 19 "Mobile
 * visual rule": "Use the LOOP-MIND visual language. Do not create a
 * separate mobile product theme." React Native has no CSS, so these are
 * the same token values as plain JS constants rather than custom-property
 * overrides — the source of truth (the hex values) is identical.
 */
export const colors = {
  bg: "#0F1317",
  chrome: "#12171B",
  surface: "#161C21",
  rowAlt: "#1A2126",
  raised: "#1D242A",

  border: "#232B31",
  borderHi: "#2C353B",

  text: "#F2F5F4",
  textSoft: "#C9D2CF",
  textMute: "#8A9591",

  accent: "#6FD3C0",
  accentSoft: "#97E2D4",
  accentDeep: "#3F8478",
  accentWash: "rgba(111, 211, 192, 0.14)",

  warn: "#E0A86B",
  warnWash: "rgba(224, 168, 107, 0.14)",

  danger: "#E77E72",
  dangerWash: "rgba(231, 126, 114, 0.14)",
};

export const radius = { sm: 10, lg: 14 };

export const spacing = { xs: 6, sm: 10, md: 14, lg: 18, xl: 24 };

export const fontSizes = { xs: 11, sm: 13, base: 15, md: 16, lg: 18, xl: 22, xxl: 28 };
