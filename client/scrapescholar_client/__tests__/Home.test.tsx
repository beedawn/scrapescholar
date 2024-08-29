// __tests__/Home.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../app/page'; 
import React from 'react';

describe('Home Component', () => {
    const testInput = "test input"
  test('check + button loads', () => {
    render(<Home />);
    //finds + button
    const addButton = screen.getByText('+');
    expect(addButton).toBeInTheDocument(); 
  });


  test('check ScrapeScholar heading loads', () => {
    render(<Home />);
    //checks how many input boxes there are 
    expect(screen.getByText('ScrapeScholar')).toBeInTheDocument(); 
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
    fireEvent.change(inputs[0], { target: { value: testInput} });
    expect(inputs[0]).toHaveValue(testInput);
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
    fireEvent.change(inputs[0], { target: { value: testInput } });
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    expect(screen.getByText('You searched '+ testInput)).toBeInTheDocument()
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
    fireEvent.change(firstInput, { target: { value: testInput } });
    fireEvent.change(secondInput, { target: { value: testInput +' 2' } });
    fireEvent.click(firstDeleteButton);
    expect(screen.getAllByRole('textbox')).toHaveLength(1); 
    expect(screen.getAllByRole('textbox')[0]).toHaveValue(testInput +' 2' )
  });

  test('deletes empty inputs', () => {
    render(<Home />);
    const addButton = screen.getByText('+');
    let i =0;
    while (i<6){
    fireEvent.click(addButton);
    i++}
    expect(screen.getAllByRole('textbox')).toHaveLength(i+1);

    const inputs = screen.getAllByRole('textbox');
    const firstInput = inputs[0]
    const secondInput = inputs[4]
    fireEvent.change(firstInput, { target: { value: testInput } });
    fireEvent.change(secondInput, { target: { value: testInput+' 4' } });

    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
   
    expect(screen.getAllByRole('textbox')).toHaveLength(2); 
    expect(screen.getAllByRole('textbox')[0]).toHaveValue(testInput)
    expect(screen.getAllByRole('textbox')[1]).toHaveValue(testInput+' 4')
  });


  test('blank search prompts to enter a keyword search', () => {
    render(<Home />);
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    expect(screen.getByText('Please enter a keyword')).toBeInTheDocument(); 
 
  });


});
