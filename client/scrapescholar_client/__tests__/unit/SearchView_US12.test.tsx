import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';

import fetchMock from '../helperFunctions/apiMock';

beforeEach(() => {
  global.fetch = fetchMock;
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView US-11 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"

  const accordianContainsSources = () =>{
    const scienceDirectChecklist = screen.getByText('ScienceDirect');
    const scopusChecklist = screen.getByText('Scopus');
    expect(scienceDirectChecklist).toBeInTheDocument();
    expect(scopusChecklist).toBeInTheDocument();
  }

  const clickAccordian = () =>{
    const sourcesAccordian = screen.getByText('Sources');
    fireEvent.click(sourcesAccordian);
  }

  //us-12 tests
  test('US-12 check sources accordian loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);

    const sourcesAccordian = screen.getByText('Sources');
    expect(sourcesAccordian).toBeInTheDocument();
  });

  test('US-12 press sources accordian', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);

    clickAccordian();

    await waitFor(() => {
accordianContainsSources()
  }, {timeout:5000});


  });

  test('US-12 press sources accordian twice', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const sourcesAccordian = screen.getByText('Sources');
    clickAccordian();
    await waitFor(()=>{
      accordianContainsSources();
    },{timeout:5000})
    fireEvent.click(sourcesAccordian);
    expect(sourcesAccordian).toBeInTheDocument();
  });

  test('US-12 check checkboxes next to source items', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    clickAccordian();
    await waitFor(()=>{
      accordianContainsSources();
    },{timeout:5000})
    const scienceDirectCheckbox = screen.getByRole('checkbox', { name: /ScienceDirect/i });
    const scopusCheckbox = screen.getByRole('checkbox', { name: /Scopus/i });
    expect(scienceDirectCheckbox).toBeInTheDocument();
    expect(scopusCheckbox).toBeInTheDocument();
  });

  test('US-12 ensure checkboxes are initially checked ', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    clickAccordian();
    await waitFor(()=>{
      accordianContainsSources();
    })
    const scienceDirectCheckbox = screen.getByRole('checkbox', { name: /ScienceDirect/i });
    const scopusCheckbox = screen.getByRole('checkbox', { name: /Scopus/i });
    expect(scienceDirectCheckbox).toBeChecked();
    expect(scopusCheckbox).toBeChecked();
  });

  test('US-12 ensure checkboxes can be unchecked ', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    clickAccordian();
    await waitFor(()=>{
      accordianContainsSources();
    })
    const scienceDirectCheckbox = screen.getByRole('checkbox', { name: /ScienceDirect/i });
    const scopusCheckbox = screen.getByRole('checkbox', { name: /Scopus/i });
    fireEvent.click(scienceDirectCheckbox);
    fireEvent.click(scopusCheckbox);
    expect(scienceDirectCheckbox).not.toBeChecked();
    expect(scopusCheckbox).not.toBeChecked();

  });

});
