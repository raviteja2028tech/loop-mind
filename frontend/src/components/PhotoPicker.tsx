import * as Popover from "@radix-ui/react-popover";
import { Camera, File as FileIcon, Image as ImageIcon } from "lucide-react";
import * as React from "react";

/**
 * Profile Photo — Selection Interaction (spec.md §8, repeated at the My
 * Profile "Change Photo" control): clicking the Profile Photo control
 * must open a selection interface offering exactly Camera / Photos /
 * Files, each with a matching icon in the established visual style.
 *
 * All three ultimately open the browser's own file picker — the one real
 * distinction the web platform offers is the `capture` attribute, which
 * nudges a mobile browser to open the camera directly for "Camera" and
 * skip it for "Photos"/"Files". This is the honest ceiling of what a web
 * page can do; it does not claim OS-level camera/gallery/file-system
 * separation beyond what `capture` actually provides.
 */
export function PhotoPicker({
  onFiles,
  trigger,
}: {
  onFiles: (files: File[]) => void;
  trigger: React.ReactNode;
}) {
  const [open, setOpen] = React.useState(false);
  const cameraRef = React.useRef<HTMLInputElement>(null);
  const photosRef = React.useRef<HTMLInputElement>(null);
  const filesRef = React.useRef<HTMLInputElement>(null);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files.length > 0) {
      onFiles(Array.from(e.target.files));
    }
    e.target.value = "";
    setOpen(false);
  }

  return (
    <Popover.Root open={open} onOpenChange={setOpen}>
      <Popover.Trigger asChild>{trigger}</Popover.Trigger>
      <Popover.Portal>
        <Popover.Content align="start" sideOffset={6} className="lm-popover z-[70] w-[180px]">
          <div className="flex flex-col gap-1">
            <button
              type="button"
              className="lm-nav-link flex items-center gap-2 !justify-start"
              onClick={() => cameraRef.current?.click()}
            >
              <Camera className="size-4" /> Camera
            </button>
            <button
              type="button"
              className="lm-nav-link flex items-center gap-2 !justify-start"
              onClick={() => photosRef.current?.click()}
            >
              <ImageIcon className="size-4" /> Photos
            </button>
            <button
              type="button"
              className="lm-nav-link flex items-center gap-2 !justify-start"
              onClick={() => filesRef.current?.click()}
            >
              <FileIcon className="size-4" /> Files
            </button>
          </div>
        </Popover.Content>
      </Popover.Portal>

      <input
        ref={cameraRef}
        type="file"
        accept="image/*"
        capture="user"
        className="hidden"
        onChange={handleChange}
      />
      <input
        ref={photosRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleChange}
      />
      <input
        ref={filesRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleChange}
      />
    </Popover.Root>
  );
}
