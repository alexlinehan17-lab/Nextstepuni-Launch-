import React from 'react';
import { describe, expect, test } from 'vitest';
import { render } from '@testing-library/react';

import NorthStarCategoryIcon from '@/components/NorthStarCategoryIcon';

describe('NorthStarCategoryIcon', () => {
  test('uses the onboarding illustration and painted blob for the selected category', () => {
    const { container, rerender } = render(
      <NorthStarCategoryIcon category="options-freedom" size={80} />,
    );

    expect(container.querySelector('img')).toHaveAttribute('src', '/icons/north-star/open-options.png');
    expect(container.querySelector('path')).toHaveAttribute('fill', '#B5D4CC');

    rerender(<NorthStarCategoryIcon category="family-community" size={80} />);
    expect(container.querySelector('img')).toHaveAttribute('src', '/icons/north-star/community.png');
    expect(container.querySelector('path')).toHaveAttribute('fill', '#ECBBCC');
  });
});
