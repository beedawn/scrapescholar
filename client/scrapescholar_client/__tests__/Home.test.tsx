// __tests__/Home.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Home from '../app/page'; // Adjust the import path
import React from 'react';

describe('Home Component', () => {
  test('renders initial text', () => {
    render(<Home />);
    expect(screen.getByText('hello world!')).toBeInTheDocument();
  });

  test('adds new input field on "+" button click', () => {
    render(<Home />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    expect(screen.getAllByRole('textbox')).toHaveLength(2); // Assuming the initial state has 1 input
  });

  test('updates input value correctly', () => {
    render(<Home />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test input' } });
    expect(input).toHaveValue('test input');
  });
});
