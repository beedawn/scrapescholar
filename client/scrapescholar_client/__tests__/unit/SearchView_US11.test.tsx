import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import fetchMock from '../helperFunctions/apiMock';
import submitSearch from '../helperFunctions/submitSearch';

beforeEach(() => {
    global.fetch = fetchMock;
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView US-11 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"


  //US-11
  test('US-11 shows No results found after search press', async () => {
    //sets empty response from api
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve(
          []
        ),
        headers: new Headers(),
        redirected: false,
        statusText: 'OK',
      })
    ) as jest.Mock;

    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    await waitFor(() => {
    submitSearch(testInput);
}, { timeout: 5000 });
    screen.debug()
    await waitFor(() => {
      expect(screen.getByText('No Results Found')).toBeInTheDocument()
    }, { timeout: 5000 });
  })

  test('US-11 shows link in response after search press', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const sourcesAccordian = screen.getByText('Sources');
    fireEvent.click(sourcesAccordian);
    await waitFor(() => {
        const scienceDirectChecklist = screen.getByText('ScienceDirect');
        const scopusChecklist = screen.getByText('Scopus');
        expect(scienceDirectChecklist).toBeInTheDocument();
        expect(scopusChecklist).toBeInTheDocument();
    }, {timeout:5000});

    submitSearch(testInput);

    await waitFor(() => {
      expect(screen.getByText('link a')).toBeInTheDocument()
      expect(screen.getByText('link x')).toBeInTheDocument()
    }, { timeout: 5000 });
    screen.debug();
  })

});
