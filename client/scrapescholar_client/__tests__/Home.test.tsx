// __tests__/Home.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../app/page'; 
import React from 'react';

describe('Home Component', () => {

  test('check + button loads', () => {
    render(<Home />);
    //finds + button
    const addButton = screen.getByText('+');
    expect(addButton).toBeInTheDocument(); 
  });

  test('check SearchBox loads', () => {
    render(<Home />);
    //checks how many input boxes there are 
    expect(screen.getAllByRole('textbox')).toHaveLength(1); 
  });

  test('check - button loads', () => {
    render(<Home />);
    //finds - button
    const deleteButton = screen.getByText('-');
    expect(deleteButton).toBeInTheDocument(); 
  });

  test('adds new input field on "+" button click', () => {
    render(<Home />);
    const addButton = screen.getByText('+');
    //clicks + button
    fireEvent.click(addButton);
    //should be 2 inputs now
    expect(screen.getAllByRole('textbox')).toHaveLength(2); 
    //maybe should test there are two + buttons too?
  });

  test('updates input value correctly', () => {
    render(<Home />);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: 'test input' } });
    expect(inputs[0]).toHaveValue('test input');
  });

  test('shows No results found after search press', () =>{
    render(<Home />);
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    expect(screen.getByText('No results found.')).toBeInTheDocument()
  })

  test('shows you searched test input after search press', () =>{
    render(<Home />);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: 'test input' } });
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    expect(screen.getByText('You searched test input')).toBeInTheDocument()
  })

  test('removes input when delete button clicked', () => {
    render(<Home />);
    const addButton = screen.getByText('+');
    const deleteButton = screen.getAllByText('-');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    const firstInput = inputs[0]
    const secondInput = inputs[1]
    const firstDeleteButton = deleteButton[0]
    fireEvent.change(firstInput, { target: { value: 'test input' } });
    fireEvent.change(secondInput, { target: { value: 'test input 2' } });
    fireEvent.click(firstDeleteButton);
    expect(screen.getAllByRole('textbox')).toHaveLength(1); 
    expect(screen.getAllByRole('textbox')[0]).toHaveValue('test input 2')
  });
});
