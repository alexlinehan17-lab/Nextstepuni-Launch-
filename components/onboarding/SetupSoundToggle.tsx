import React from "react";
import { Volume2, VolumeX } from "lucide-react";
import { setSoundMuted, useSoundMuted } from "../approved-ui-runtime";

export default function SetupSoundToggle() {
  const muted = useSoundMuted();
  if (typeof globalThis.AudioContext !== "function") return null;
  return (
    <button
      type="button"
      className="setup-sound-toggle"
      aria-label={muted ? "Turn interface sound on" : "Turn interface sound off"}
      aria-pressed={!muted}
      title={muted ? "Sound off" : "Sound on"}
      data-sound="swoosh"
      onClick={() => setSoundMuted(!muted)}
    >
      {muted ? <VolumeX size={17} aria-hidden="true" /> : <Volume2 size={17} aria-hidden="true" />}
      <span>Sound {muted ? "off" : "on"}</span>
    </button>
  );
}
