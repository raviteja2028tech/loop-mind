import * as React from "react";
import { cn } from "@/lib/cn";

/** Upload / dropzone — spec.md §20. */
export function Dropzone({
  onFiles,
  accept,
  multiple = false,
  hint,
  className,
}: {
  onFiles: (files: File[]) => void;
  accept?: string;
  multiple?: boolean;
  hint?: string;
  className?: string;
}) {
  const [active, setActive] = React.useState(false);
  const inputRef = React.useRef<HTMLInputElement>(null);

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => inputRef.current?.click()}
      onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        setActive(true);
      }}
      onDragLeave={() => setActive(false)}
      onDrop={(e) => {
        e.preventDefault();
        setActive(false);
        onFiles(Array.from(e.dataTransfer.files));
      }}
      className={cn("lm-dropzone", active && "is-active", className)}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        multiple={multiple}
        className="hidden"
        onChange={(e) => e.target.files && onFiles(Array.from(e.target.files))}
      />
      {hint ?? "Drop a file or click to browse"}
    </div>
  );
}
