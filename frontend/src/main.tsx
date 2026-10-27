import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
// Centralized Graphite Ink theme (imports Tailwind's base layer first,
// then the design tokens/components) — spec.md §32 "Implementation Rule".
import "./styles/agenthire-theme.css";
// React Flow's base styles — needed wherever the AI Recruitment Workflow
// visualization (phase.md Phase 13) renders a <ReactFlow> diagram.
import "reactflow/dist/style.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
