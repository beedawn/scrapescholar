// __tests__/Home.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../app/page'; 
import {handleSearchChange} from '../app/page';
import React from 'react';

describe('Home Component', () => {
  test('renders initial hello world text', () => {
    render(<Home />);
    expect(screen.getByText('hello world!')).toBeInTheDocument();
  });

  test('check + button loads', () => {
    render(<Home />);
    const addButton = screen.getByText('+');
    expect(addButton).toBeInTheDocument(); 
  });

  test('check SearchBox loads', () => {
    render(<Home />);
    expect(screen.getAllByRole('textbox')).toHaveLength(1); 
  });

  test('adds new input field on "+" button click', () => {
    render(<Home />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    expect(screen.getAllByRole('textbox')).toHaveLength(2); 
  });

  test('updates input value correctly', () => {
    render(<Home />);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: 'test input' } });
    expect(inputs[0]).toHaveValue('test input');
  });
});
