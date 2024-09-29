import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, { ResultItem } from '../../app/views/SearchView';
import React from 'react';


import itemsJson from '../ItemsTestJson';

import sourcesJson from '../DatabaseSourcesJson';


beforeEach(() => {


    global.fetch = jest.fn((url) => {
        const academic_database_url = /^http:\/\/0.0.0.0:8000\/academic_data\?keywords\=/
  
        const academic_sources_url =/^http:\/\/0.0.0.0:8000\/academic_sources/
        if (academic_database_url.test(url)) {
          return Promise.resolve({
                ok: true,
                status: 200,
                json: () => Promise.resolve(itemsJson),
                headers: new Headers(),
                redirected: false,
                statusText: 'OK',
          
              })
        
    
    }
        if (academic_sources_url.test(url)) {
          return Promise.resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve(sourcesJson),
            headers: new Headers(),
            redirected: false,
            statusText: 'OK',
            
          });
        }
        return Promise.reject(new Error('Invalid URL'));
    }) as jest.Mock;
//   // Reset mocks before each test
//   global.fetch = jest.fn(() =>
//     Promise.resolve({
//       ok: true,
//       status: 200,
//       json: () => Promise.resolve(itemsJson),
//       headers: new Headers(),
//       redirected: false,
//       statusText: 'OK',

//     })
//   ) as jest.Mock;
  
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView US-11 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"


  //US-11
  test('US-11 shows No results found after search press', async () => {
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
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
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


    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');

    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(screen.getByText('link a')).toBeInTheDocument()
      expect(screen.getByText('link x')).toBeInTheDocument()
    }, { timeout: 5000 });
    screen.debug();
  })

});
