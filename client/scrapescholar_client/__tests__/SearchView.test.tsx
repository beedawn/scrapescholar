// __tests__/SearchView.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../app/views/SearchView';
import React from 'react';

describe('Home Component', () => {
  const testInput = "test input"
  test('check + button loads', () => {
    render(<SearchView />);
    //finds + button
    const addButton = screen.getByText('+');
    expect(addButton).toBeInTheDocument();
  });


  test('check ScrapeScholar heading loads', () => {
    render(<SearchView />);
    //checks how many input boxes there are 
    expect(screen.getByText('ScrapeScholar')).toBeInTheDocument();
  });

  test('check SearchBox loads', () => {
    render(<SearchView />);
    //checks how many input boxes there are 
    expect(screen.getAllByRole('textbox')).toHaveLength(1);
  });

  test('check - button loads', () => {
    render(<SearchView />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton)
    //finds - button
    const deleteButton = screen.getByText('-');
    expect(deleteButton).toBeInTheDocument();
  });

  test('adds new input field on "+" button click', () => {
    render(<SearchView />);
    const addButton = screen.getByText('+');
    //clicks + button
    fireEvent.click(addButton);
    //should be 2 inputs now
    expect(screen.getAllByRole('textbox')).toHaveLength(2);
    //maybe should test there are two + buttons too?
  });

  test('updates input value correctly', () => {
    render(<SearchView />);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    expect(inputs[0]).toHaveValue(testInput);
  });

  test('shows No results found after search press', () => {
    render(<SearchView />);
    const searchButton = screen.getByText('Search');

    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    expect(screen.getByText('No results found.')).toBeInTheDocument()
  })

  test('shows you searched test input after search press', () => {
    render(<SearchView />);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    expect(screen.getByText('You searched ' + testInput)).toBeInTheDocument()
  })

  test('removes input when delete button clicked', () => {
    render(<SearchView />);
    const addButton = screen.getByText('+');

    fireEvent.click(addButton);
    fireEvent.click(addButton);
    const deleteButton = screen.getAllByText('-');
    const inputs = screen.getAllByRole('textbox');
    const firstInput = inputs[0]
    const secondInput = inputs[1]
    const thirdInput = inputs[2]
    const firstDeleteButton = deleteButton[0]
    fireEvent.change(firstInput, { target: { value: testInput } });
    fireEvent.change(secondInput, { target: { value: testInput + ' 2' } });
    fireEvent.change(thirdInput, { target: { value: testInput + ' 3' } });
    fireEvent.click(firstDeleteButton);
    expect(screen.getAllByRole('textbox')).toHaveLength(2);
    expect(screen.getAllByRole('textbox')[1]).toHaveValue(testInput + ' 3')
  });

  test('deletes empty inputs', () => {
    render(<SearchView />);
    const addButton = screen.getByText('+');
    let i = 0;
    while (i < 6) {
      fireEvent.click(addButton);
      i++
    }
    expect(screen.getAllByRole('textbox')).toHaveLength(i + 1);

    const inputs = screen.getAllByRole('textbox');
    const firstInput = inputs[0]
    const secondInput = inputs[4]
    fireEvent.change(firstInput, { target: { value: testInput } });
    fireEvent.change(secondInput, { target: { value: testInput + ' 4' } });

    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);

    expect(screen.getAllByRole('textbox')).toHaveLength(2);
    expect(screen.getAllByRole('textbox')[0]).toHaveValue(testInput)
    expect(screen.getAllByRole('textbox')[1]).toHaveValue(testInput + ' 4')
  });


  test('blank search prompts to enter a keyword search', () => {
    render(<SearchView />);
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    expect(screen.getByText('Please enter a keyword')).toBeInTheDocument();

  });


});
