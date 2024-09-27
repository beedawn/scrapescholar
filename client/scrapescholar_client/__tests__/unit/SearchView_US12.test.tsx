import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, { ResultItem } from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';
import { sortResults } from '../../app/components/SearchView/ResultsTable';

import itemsArray from '../ItemsTestArray';
import itemsJson from '../ItemsTestJson';

const items: ResultItem[] = itemsArray;

beforeEach(() => {
  // Reset mocks before each test
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(itemsJson),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',

    })
  ) as jest.Mock;
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView US-11 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"

 


  //us-12 tests
  test('US-12 check sources accordian loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);

    const sourcesAccordian = screen.getByText('Sources');
    expect(sourcesAccordian).toBeInTheDocument();
  });

  test('US-12 press sources accordian', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);

    const sourcesAccordian = screen.getByText('Sources');
    fireEvent.click(sourcesAccordian);
    const scienceDirectChecklist = screen.getByText('ScienceDirect');
    const scopusChecklist = screen.getByText('Scopus');
    expect(scienceDirectChecklist).toBeInTheDocument();
    expect(scopusChecklist).toBeInTheDocument();
  });

  test('US-12 press sources accordian twice', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);

    const sourcesAccordian = screen.getByText('Sources');
    fireEvent.click(sourcesAccordian);

    const scienceDirectChecklist = screen.getByText('ScienceDirect');
    const scopusChecklist = screen.getByText('Scopus');
    expect(scienceDirectChecklist).toBeInTheDocument();
    expect(scopusChecklist).toBeInTheDocument();
    fireEvent.click(sourcesAccordian);
    expect(sourcesAccordian).toBeInTheDocument();
  });

  test('US-12 check checkboxes next to source items', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const sourcesAccordian = screen.getByText('Sources');
    fireEvent.click(sourcesAccordian);
    const scienceDirectCheckbox = screen.getByRole('checkbox', { name: /ScienceDirect/i });
    const scopusCheckbox = screen.getByRole('checkbox', { name: /Scopus/i });
    expect(scienceDirectCheckbox).toBeInTheDocument();
    expect(scopusCheckbox).toBeInTheDocument();
  });

  test('US-12 ensure checkboxes are initially checked ', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const sourcesAccordian = screen.getByText('Sources');
    fireEvent.click(sourcesAccordian);
    const scienceDirectCheckbox = screen.getByRole('checkbox', { name: /ScienceDirect/i });
    const scopusCheckbox = screen.getByRole('checkbox', { name: /Scopus/i });
    expect(scienceDirectCheckbox).toBeChecked();
    expect(scopusCheckbox).toBeChecked();
  });

  test('US-12 ensure checkboxes can be unchecked ', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const sourcesAccordian = screen.getByText('Sources');
    fireEvent.click(sourcesAccordian);
    const scienceDirectCheckbox = screen.getByRole('checkbox', { name: /ScienceDirect/i });
    const scopusCheckbox = screen.getByRole('checkbox', { name: /Scopus/i });
    fireEvent.click(scienceDirectCheckbox);
    fireEvent.click(scopusCheckbox);
    expect(scienceDirectCheckbox).not.toBeChecked();
    expect(scopusCheckbox).not.toBeChecked();

  });

});
