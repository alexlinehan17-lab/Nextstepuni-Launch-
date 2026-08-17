import React from 'react';
import type { NorthStarCategory } from '../types';

export interface NorthStarCategoryIconConfig {
  iconPath: string;
  blob: string;
  blobPath: string;
}

/**
 * The category artwork used during North Star onboarding. Keeping this in one
 * shared registry means every later North Star surface reflects the choice the
 * student actually made instead of falling back to a generic compass.
 */
export const NORTH_STAR_CATEGORY_BLOBS: Record<NorthStarCategory, NorthStarCategoryIconConfig> = {
  independence: {
    iconPath: '/icons/north-star/my-own-path.png',
    blob: '#DDC9A4',
    blobPath: 'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
  },
  'family-community': {
    iconPath: '/icons/north-star/community.png',
    blob: '#ECBBCC',
    blobPath: 'M 4 28 Q 0 56 12 82 Q 28 100 56 96 Q 90 92 96 60 Q 100 28 82 8 Q 56 -6 30 6 Q 10 16 4 28 Z',
  },
  'career-craft': {
    iconPath: '/icons/north-star/career.png',
    blob: '#F5C7A0',
    blobPath: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
  },
  'college-learning': {
    iconPath: '/icons/north-star/learning.png',
    blob: '#BCCCE3',
    blobPath: 'M 6 22 Q -2 50 10 78 Q 26 98 56 94 Q 90 88 96 56 Q 100 24 80 6 Q 56 -6 28 6 Q 10 14 6 22 Z',
  },
  'prove-myself': {
    iconPath: '/icons/north-star/prove-them-wrong.png',
    blob: '#F1B7AB',
    blobPath: 'M 4 26 Q 2 56 12 82 Q 26 98 52 96 Q 88 94 96 64 Q 100 34 84 10 Q 60 -4 30 6 Q 10 18 4 26 Z',
  },
  'options-freedom': {
    iconPath: '/icons/north-star/open-options.png',
    blob: '#B5D4CC',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
  },
  'family-people': {
    iconPath: '/icons/north-star/community.png',
    blob: '#ECBBCC',
    blobPath: 'M 4 28 Q 0 56 12 82 Q 28 100 56 96 Q 90 92 96 60 Q 100 28 82 8 Q 56 -6 30 6 Q 10 16 4 28 Z',
  },
  'prove-myself-jc': {
    iconPath: '/icons/north-star/prove-them-wrong.png',
    blob: '#F1B7AB',
    blobPath: 'M 4 26 Q 2 56 12 82 Q 26 98 52 96 Q 88 94 96 64 Q 100 34 84 10 Q 60 -4 30 6 Q 10 18 4 26 Z',
  },
  'curiosity-craft': {
    iconPath: '/icons/north-star/career.png',
    blob: '#F5C7A0',
    blobPath: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
  },
  'future-doors': {
    iconPath: '/icons/north-star/open-options.png',
    blob: '#B5D4CC',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
  },
};

interface CategoryIconBlobProps {
  config: NorthStarCategoryIconConfig;
  size: number;
  className?: string;
}

/** The illustration deliberately exceeds the painted blob by a few pixels. */
export const CategoryIconBlob: React.FC<CategoryIconBlobProps> = ({ config, size, className }) => (
  <div
    className={`relative shrink-0 ${className ?? ''}`}
    style={{ width: size, height: size, overflow: 'visible' }}
    aria-hidden="true"
  >
    <svg
      className="absolute pointer-events-none"
      viewBox="0 0 100 100"
      preserveAspectRatio="xMidYMid meet"
      style={{
        width: '88%',
        height: '88%',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 0,
      }}
    >
      <path d={config.blobPath} fill={config.blob} opacity="0.85" />
    </svg>
    <img
      src={config.iconPath}
      alt=""
      style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        width: '105%',
        height: '105%',
        objectFit: 'contain',
        zIndex: 1,
      }}
      draggable={false}
    />
  </div>
);

interface NorthStarCategoryIconProps {
  category: NorthStarCategory;
  size?: number;
  className?: string;
}

export const NorthStarCategoryIcon: React.FC<NorthStarCategoryIconProps> = ({
  category,
  size = 72,
  className,
}) => (
  <CategoryIconBlob config={NORTH_STAR_CATEGORY_BLOBS[category]} size={size} className={className} />
);

export default NorthStarCategoryIcon;
