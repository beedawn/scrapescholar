import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, { ResultItem } from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';
import { sortResults } from '../../app/components/SearchView/ResultsTable';

/*

    id: number;
    title: string;
    link: string;
    date: string;
    source: string;
    citedby:number;
    color:string;
    relevance:number;
    abstract: string;
    doctype: string;
    evaluation_criteria: string;
    methodology: number;
    clarity: 0;
    completeness: 0;
    transparency: 0;*/
const items: ResultItem[] = [
  {
    id: 0,
    title: "test 1",
    link: "link x",
    date: "2024-05-31",
    source: "Science Direct",
    citedby: 0,
    color: "red",
    relevance_score: 92,
    abstract: "a",
    document_type: "article",
    evaluation_criteria: "accept",
    methodology: "0",
    clarity: "0",
    transparency: "0",
    completeness: "0"
  },
  {
    id: 1,
    title: "test 2",
    link: "link a",
    date: "2024-07-01",
    source: "Scopus",
    citedby: 1,
    color: "yellow",
    relevance_score: 80,
    abstract: "b",
    document_type: "journal",
    evaluation_criteria: "deny",
    methodology: "1",
    clarity: "1",
    transparency: "1",
    completeness: "1"
  },
  {
    id: 1,
    title: "test 1",
    link: "link a",
    date: "2024-07-01",
    source: "Scopus",
    citedby: 1,
    color: "yellow",
    relevance_score: 80,
    abstract: "b",
    document_type: "journal",
    evaluation_criteria: "deny",
    methodology: "1",
    clarity: "1",
    transparency: "1",
    completeness: "1"
  }
]

beforeEach(() => {
  // Reset mocks before each test
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(
        [
          {
            "id": "0",
            "title": "test 1",
            "link": "link x",
            "date": "2024-05-31",
            "source": "Science Direct",
            "citedby": "0",
            "color": "red",
            "relevance_score": "92",
            "abstract": "a",
            "document_type": "article",
            "evaluation_criteria": "accept",
            "methodology": "0",
            "clarity": "0",
            "transparency": "0",
            "completeness": "0"
          },
          {
            "id": "1",
            "title": "test 2",
            "link": "link a",
            "date": "2024-07-01",
            "source": "Scopus",
            "citedby": "1",
            "color": "yellow",
            "relevance_score": "80",
            "abstract": "b",
            "document_type": "journal",
            "evaluation_criteria": "deny",
            "methodology": "1",
            "clarity": "1",
            "transparency": "1",
            "completeness": "1"
          }
        ]
      ),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',

    })
  ) as jest.Mock;
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView US-4 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"
  test('US-4 check logout button renders in SearchView', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const logoutButton = screen.getByText('Logout');
    expect(logoutButton).toBeInTheDocument();
  });
});
