import React, { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { NORTH_STAR_CATEGORY_BLOBS } from "../NorthStarCategoryIcon";

/** Keep the outgoing artwork visible until its replacement has loaded. */
export default function NorthStarArtwork({
  src,
  label,
  reduced,
}: {
  src: string;
  label: string;
  reduced: boolean | null;
}) {
  const [shown, setShown] = useState({ src, label });
  useEffect(() => {
    Object.values(NORTH_STAR_CATEGORY_BLOBS).forEach((art) => {
      const image = new Image();
      image.src = art.iconPath;
    });
  }, []);
  useEffect(() => {
    let active = true;
    const image = new Image();
    image.onload = () => {
      if (active) setShown({ src, label });
    };
    image.src = src;
    return () => {
      active = false;
    };
  }, [src, label]);
  return (
    <div className="desk-north-art" aria-hidden="true">
      <AnimatePresence initial={false}>
        <motion.div
          key={shown.src}
          className="desk-art-layer"
          initial={{ opacity: 0, y: reduced ? 0 : 6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: reduced ? 0 : -4 }}
          transition={{
            duration: reduced ? 0 : 0.28,
            ease: [0.22, 1, 0.36, 1],
          }}
        >
          <img src={shown.src} alt="" />
          <span className="desk-art-note">{shown.label}</span>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
