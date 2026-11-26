import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';
import hoverOnlyWhenSupported from './design/postcss-hover-only.js';

export default {
  plugins: [
    tailwindcss(),
    // After Tailwind: guards every hand-written :hover rule the way
    // future.hoverOnlyWhenSupported guards Tailwind's own (tailwind.config.ts).
    hoverOnlyWhenSupported(),
    autoprefixer(),
  ],
};
