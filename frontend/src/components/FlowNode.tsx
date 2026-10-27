import { Handle, Position } from "reactflow";
import { cn } from "@/lib/cn";

/** Workflow node states — spec.md §24 + §3.1 (live AI workflow visualization). */
export type FlowNodeState =
  "pending" | "running" | "completed" | "failed" | "paused" | "approved" | "rejected";

export interface FlowNodeData {
  label: string;
  state: FlowNodeState;
}

export function FlowNode({ data }: { data: FlowNodeData }) {
  return (
    <div className={cn("lm-flow-node")} data-state={data.state}>
      <Handle type="target" position={Position.Left} />
      <div className="flex items-center justify-between gap-2">
        <span>{data.label}</span>
        <span className="uppercase opacity-70">{data.state}</span>
      </div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
}

export const flowNodeTypes = { workflow: FlowNode };
