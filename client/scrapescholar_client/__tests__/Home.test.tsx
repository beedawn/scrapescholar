// __tests__/SearchView.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../app/page';
import React from 'react';

describe('Home Component', () => {
  const testInput = "test input"
  test('check login button loads', () => {
    render(<Home />);
    //finds + button
    const loginButton = screen.getByText('Login');
    expect(loginButton).toBeInTheDocument();
  });

  test('adds new input field on "+" button click', () => {
    render(<Home />);
    const loginButton = screen.getByText('Login');
    //clicks + button
    fireEvent.click(loginButton);
    //should be 2 inputs now
    expect(screen.getAllByRole('textbox')).toHaveLength(1);
    expect(screen.getByText('ScrapeScholar')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
    //maybe should test there are two + buttons too?
  });


});
