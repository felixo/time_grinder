import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import { HomePage } from './HomePage';

test('renders the Time Grinder landing page', () => {
  render(<HomePage />);

  expect(screen.getByRole('heading', { name: 'Time Grinder', level: 1 })).toBeVisible();
  expect(screen.getByText('Time tracking is coming soon.')).toBeVisible();
});
