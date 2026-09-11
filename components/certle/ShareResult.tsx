import React, { useEffect, useState } from "react";
import { Copy, Download, Mail, Share2 } from "lucide-react";
import { CertleLogo } from "./CertleIdentity";
import {
  createResultImage,
  socialShareUrl,
  type ResultShareData,
  type SharePlatform,
} from "./sharing";

function SocialIcon({ platform }: { platform: SharePlatform }) {
  const paths: Record<SharePlatform, string> = {
    Facebook:
      "M13.5 21v-8h2.8l.4-3.2h-3.2v-2c0-.9.3-1.6 1.6-1.6h1.7V3.4a23 23 0 0 0-2.5-.1c-2.5 0-4.2 1.5-4.2 4.3v2.2H7.3V13h2.8v8z",
    LinkedIn:
      "M5.5 8.5H2.8V21h2.7zM4.2 3a1.7 1.7 0 1 0 0 3.4 1.7 1.7 0 0 0 0-3.4M21 13.7c0-3.7-2-5.4-4.6-5.4-2.1 0-3 1.1-3.5 1.9V8.5h-2.7V21h2.7v-7c0-1.9.8-3 2.5-3s2.8 1.1 2.8 3v7H21z",
    X: "M18.9 2H22l-6.8 7.8L23.2 22h-6.3L12 14.5 5.4 22H2.2l8.3-9.5L2.8 2h6.4l4.5 6.9zM17.9 20h1.7L8.2 4H6.4z",
    WhatsApp:
      "M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2m0 2a8 8 0 1 1-4.1 14.9l-.4-.2-2.6.7.7-2.6-.2-.4A8 8 0 0 1 12 4m-3.4 3c-.3 0-.6.1-.8.4-.5.5-.8 1.1-.8 1.8 0 2.6 3.9 6.8 7.1 7.1.9.1 1.8-.3 2.3-1 .2-.4.3-1.1.2-1.3l-2.2-1c-.2-.1-.4-.1-.6.2l-.9 1c-.2.1-.4.1-.7 0-1.5-.7-2.6-1.7-3.3-3-.2-.3-.1-.5 0-.6l.6-.7c.2-.2.2-.4.1-.6l-.9-2c-.1-.3-.3-.3-.6-.3z",
  };
  return (
    <svg
      viewBox="0 0 24 24"
      width="21"
      height="21"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d={paths[platform]} />
    </svg>
  );
}

export default function ShareResult({ data }: { data: ResultShareData }) {
  const [notice, setNotice] = useState("");
  const [fallback, setFallback] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState("");
  const [imageError, setImageError] = useState(false);
  useEffect(() => {
    let active = true;
    createResultImage(data)
      .then((value) => {
        if (active) setFile(value);
      })
      .catch(() => {
        if (active) setImageError(true);
      });
    return () => {
      active = false;
    };
  }, [data]);
  useEffect(() => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    setImageUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);
  const copy = async (paste = false) => {
    try {
      await navigator.clipboard.writeText(data.text);
      setNotice(
        paste
          ? "Result copied. Paste it into your post."
          : "Result copied. Ready to paste.",
      );
    } catch {
      setFallback(true);
      setNotice("Select and copy your result below.");
    }
  };
  const nativeShare = async () => {
    if (typeof navigator.share !== "function") {
      await copy();
      return;
    }
    try {
      await navigator.share(
        file && navigator.canShare?.({ files: [file] })
          ? { files: [file], title: "My CERTLE result", text: data.text }
          : { title: "My CERTLE result", text: data.text },
      );
    } catch (error) {
      if ((error as Error).name !== "AbortError") await copy();
    }
  };
  const download = () => {
    if (!file) return;
    const url = URL.createObjectURL(file),
      a = document.createElement("a");
    a.href = url;
    a.download = file.name;
    a.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 30000);
    setNotice("Image saved. Add it to a post or story.");
  };
  return (
    <div className="certle-share-panel">
      <p className="certle-share-intro">
        Same question. See how your friends do.
      </p>
      {imageUrl ? (
        <img
          className="certle-share-image"
          src={imageUrl}
          alt={`CERTLE ${data.number}. ${data.earned} of ${data.total} marks in ${data.attempts} attempts. Spoiler-free result card.`}
        />
      ) : (
        <div
          className="certle-share-card"
          aria-label={`CERTLE ${data.number}, ${data.earned} of ${data.total} marks, ${data.attempts} attempts`}
        >
          <div className="certle-share-edition">
            <span>No. {String(data.number).padStart(3, "0")}</span>
            <span>{data.subject}</span>
          </div>
          <CertleLogo />
          <strong className="certle-share-score">
            {data.earned}
            <span>/{data.total}</span>
          </strong>
          <p>marks · {data.attempts} of 3 attempts</p>
          <div className="certle-share-tiles" aria-hidden="true">
            {data.rows.map((row, i) => (
              <div key={i}>
                {row.map((hit, j) => (
                  <i key={j} className={hit ? "earned" : ""} />
                ))}
              </div>
            ))}
          </div>
          <div className="certle-share-card-foot">
            <b>Your turn.</b>
            <span>nextstepuni.com/certle</span>
          </div>
        </div>
      )}
      <nav className="certle-socials" aria-label="Share your CERTLE result">
        {(["Facebook", "LinkedIn", "X", "WhatsApp"] as const).map(
          (platform) => (
            <a
              key={platform}
              href={socialShareUrl(platform, data.text)}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`Share on ${platform}`}
              onClick={() => {
                if (platform === "Facebook" || platform === "LinkedIn")
                  void copy(true);
              }}
            >
              <span>
                <SocialIcon platform={platform} />
              </span>
              {platform}
            </a>
          ),
        )}
        <a
          href={`mailto:?subject=${encodeURIComponent(`Your turn — CERTLE #${data.number}`)}&body=${encodeURIComponent(data.text)}`}
          aria-label="Share by email"
        >
          <span>
            <Mail size={21} />
          </span>
          Email
        </a>
      </nav>
      <p className="certle-share-tip">
        Facebook & LinkedIn open a link preview. Your score is copied so you can
        paste it into your post.
      </p>
      <div className="certle-share-actions">
        <button
          className="certle-primary"
          type="button"
          onClick={() => void copy()}
        >
          <Copy size={17} />
          Copy result
        </button>
        <button
          className="certle-secondary"
          type="button"
          disabled={!file}
          onClick={download}
        >
          <Download size={17} />
          {imageError
            ? "Image unavailable"
            : file
              ? "Save image"
              : "Preparing image…"}
        </button>
        {typeof navigator.share === "function" && (
          <button
            className="certle-text-button"
            type="button"
            onClick={() => void nativeShare()}
          >
            <Share2 size={17} />
            More sharing options
          </button>
        )}
      </div>
      <p className="certle-share-notice" role="status">
        {notice}
      </p>
      {fallback && (
        <textarea
          className="certle-share-fallback"
          aria-label="Result to copy"
          readOnly
          value={data.text}
          onFocus={(e) => e.target.select()}
        />
      )}
    </div>
  );
}
