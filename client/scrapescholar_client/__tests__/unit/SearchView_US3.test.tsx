import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
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
  // UT-3.1
  test('20+ inputs denies more inputs and displays error message', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const addButton = screen.getByText('+');
    for(let i =0;i<=21;i++){
        fireEvent.click(addButton);
    }
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    expect(inputs.length).toBeLessThanOrEqual(20);
    const error_msg=/Maximum 20 keywords allowed./i;
    await waitFor(async () => {
        expect(await screen.findByText(error_msg)).toBeInTheDocument();
  });
});
});