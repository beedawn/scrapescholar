import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, { ResultItem } from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';
import { sortResults } from '../../app/components/SearchView/ResultsTable';
import itemsArray from '../mockData/ItemsTestArray';

import submitSearch from '../helperFunctions/submitSearch';
const items: ResultItem[] = itemsArray;

import apiCalls from '../../app/api/apiCalls';

import fetchMock from '../helperFunctions/apiMock';

beforeEach(() => {
  global.fetch = fetchMock;
});

afterEach(() => {
  jest.restoreAllMocks();
});



describe('SearchView Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"
  

  // UT-2.1
  test('2 inputs with text in first field displays and/or dropdown', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput + " 2" } });
    const andDropdown = screen.getByDisplayValue('AND');
    expect(andDropdown).toBeInTheDocument();
  });

    // UT-2.1
    test('checks values in AND, OR, NOT dropdown', () => {
      render(<SearchView setLoggedIn={mockSetLoggedIn} />);
      const addButton = screen.getByText('+');
      fireEvent.click(addButton);
      const inputs = screen.getAllByRole('textbox');
      fireEvent.change(inputs[0], { target: { value: testInput } });
      fireEvent.change(inputs[1], { target: { value: testInput + " 2" } });
      const andDropdown = screen.getByDisplayValue('AND');
      expect(andDropdown).toBeInTheDocument();


      const options = screen.getAllByRole('option');
      const optionValues = options.map(option => option.textContent);
      expect(optionValues).toEqual(['AND', 'OR', 'NOT']); 
    });



        // UT-2.2
        test('checks values in AND, OR, NOT dropdown', () => {
            render(<SearchView setLoggedIn={mockSetLoggedIn} />);
            const { getAPIResults } = apiCalls();
            const addButton = screen.getByText('+');
            const expectedString = `${testInput}+AND+${testInput} 2`;
            fireEvent.click(addButton);
            const inputs = screen.getAllByRole('textbox');
            fireEvent.change(inputs[0], { target: { value: testInput } });
            fireEvent.change(inputs[1], { target: { value: testInput + " 2" } });
            const andDropdown = screen.getByDisplayValue('AND');
            expect(andDropdown).toBeInTheDocument();
      
      
            const options = screen.getAllByRole('option');
            const optionValues = options.map(option => option.textContent);
            expect(optionValues).toEqual(['AND', 'OR', 'NOT']); 

            const searchButton = screen.getByText('Search');
            fireEvent.click(searchButton);
           waitFor(() => {
   

            expect(getAPIResults).toHaveBeenCalledWith(
                expect.anything(), 
                expectedString,    
                expect.anything(), 
              );
            }, { timeout: 5000 })
          });
      

});
