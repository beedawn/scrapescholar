import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, {ResultItem} from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';
import {sortResults} from '../../app/components/ResultsTable';


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
const items:ResultItem[] = [
  {
    id: 0,
    title: "test 1",
    link: "link x",
    date: "2024-05-31",
    source: "Science Direct",
    citedby: 0,
    color: "red",
    relevance: 92,
    abstract: "a",
    doctype: "article",
    evaluation_criteria: "accept",
    methodology: 0,
    clarity: 0,
    transparency: 0,
    completeness: 0
  },
  {
    id: 1,
    title: "test 2",
    link: "link a",
    date: "2024-07-01",
    source: "Scopus",
    citedby: 1,
    color: "yellow",
    relevance: 80,
    abstract: "b",
    doctype: "journal",
    evaluation_criteria: "deny",
    methodology: 1,
    clarity: 1,
    transparency: 1,
    completeness: 1
  },
  {
    id: 1,
    title: "test 1",
    link: "link a",
    date: "2024-07-01",
    source: "Scopus",
    citedby: 1,
    color: "yellow",
    relevance: 80,
    abstract: "b",
    doctype: "journal",
    evaluation_criteria: "deny",
    methodology: 1,
    clarity: 1,
    transparency: 1,
    completeness: 1
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
            "relevance": "92",
            "abstract": "a",
            "doctype": "article",
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
            "relevance": "80",
            "abstract": "b",
            "doctype": "journal",
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

describe('Home Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"
  test('check + button loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    //finds + button
    const addButton = screen.getByText('+');
    expect(addButton).toBeInTheDocument();
  });

  test('check ScrapeScholar heading loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    //checks how many input boxes there are 
    expect(screen.getByText('ScrapeScholar')).toBeInTheDocument();
  });

  test('check SearchBox loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    //checks how many input boxes there are 
    expect(screen.getAllByRole('textbox')).toHaveLength(1);
  });

  test('check - button loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton)
    //finds - button
    const deleteButton = screen.getByText('-');
    expect(deleteButton).toBeInTheDocument();
  });

  test('adds new input field on "+" button click', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const addButton = screen.getByText('+');
    //clicks + button
    fireEvent.click(addButton);
    //should be 2 inputs now
    expect(screen.getAllByRole('textbox')).toHaveLength(2);
    //maybe should test there are two + buttons too?
  });

  test('updates input value correctly', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    expect(inputs[0]).toHaveValue(testInput);
  });

  test('shows you searched test input after search press', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('You searched ' + testInput)).toBeInTheDocument()

    }, { timeout: 5000 });
  })

  test('removes input when delete button clicked', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
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
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
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

  test('blank search prompts to enter a keyword search', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('Please enter a keyword')).toBeInTheDocument();
    });
  });

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

  test('and shows in results after search submitted', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput + " 2" } });
    const andDropdown = screen.getByDisplayValue('AND');
    expect(andDropdown).toBeInTheDocument();
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    const expectedText = 'You searched ' + testInput + ' AND ' + testInput + ' 2';
    await waitFor(() => {
      //expect(screen.getByText(new RegExp(expectedText,'i') )).toBeInTheDocument()
      expect(screen.getByText('You searched ' + testInput + ' AND ' + testInput + ' 2')).toBeInTheDocument()
    }, { timeout: 5000 });
  });

  test('or shows in results after search submitted', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput + " 2" } });
    const dropdown = screen.getByDisplayValue('AND');
    // Simulate selecting the second option (OR)
    fireEvent.change(dropdown, { target: { value: Dropdown.OR } });
    expect(dropdown).toBeInTheDocument();
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('You searched ' + testInput + ' OR ' + testInput + ' 2')).toBeInTheDocument()
    }, { timeout: 5000 });
  });

  test('not shows in results after search submitted', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput + " 2" } });
    const dropdown = screen.getByDisplayValue('AND');
    // Simulate selecting the second option (OR)
    fireEvent.change(dropdown, { target: { value: Dropdown.NOT } });
    expect(dropdown).toBeInTheDocument();
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('You searched ' + testInput + ' NOT ' + testInput + ' 2')).toBeInTheDocument()
    }, { timeout: 5000 })
  },);

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
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('No Results Found')).toBeInTheDocument()
    }, { timeout: 5000 });
  })

  test('US-11 shows link in response after search press', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('link a')).toBeInTheDocument()
      expect(screen.getByText('link x')).toBeInTheDocument()
    }, { timeout: 5000 });
  })

  test('US-8 Download button in response after search press', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('Download')).toBeInTheDocument()

    }, { timeout: 5000 });
  })
  test('US-8 Download button is a link', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const downloadButton = screen.getByText('Download');
      expect(downloadButton).toHaveAttribute('href', '/csv');

    }, { timeout: 5000 });
  })


  test('AR6 Test article is selectable in the UI', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const firstRow = screen.getByText('test 1').closest('tr');
      fireEvent.click(firstRow);
      expect(firstRow).toHaveClass('bg-blue-500');

    }, { timeout: 5000 });
  })


  //US-15 When user clicks on arrow next to relevance, results are sorted by relevance
  // 

  test('US-15 When user clicks on arrow next to relevance twice, results are sorted by relevance descending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const relevanceScoreHeader = screen.getByText('Relevance Score');
      sortButton = within(relevanceScoreHeader.closest('th')).getByRole('button');
    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText('92%')).toBeInTheDocument()
      expect(within(rows[1]).queryByText('80%')).toBeInTheDocument()
    }
    else
      fail('no sort button')

  })


  test('US-15 When user clicks on arrow next to relevance, results are sorted by relevance ascending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const relevanceScoreHeader = screen.getByText('Relevance Score');
      sortButton = within(relevanceScoreHeader.closest('th')).getByRole('button');

    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText('80%')).toBeInTheDocument()
      expect(within(rows[1]).queryByText('92%')).toBeInTheDocument()
    } else
      fail('no sort button found')
  })

  test('US-15 when results load relevance arrow is light gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const relevanceScoreHeader = screen.getByText('Relevance Score');
      const sortButton = within(relevanceScoreHeader.closest('th')).getByRole('button');
      expect(sortButton).toHaveClass('bg-gray-400');
    }, { timeout: 5000 });
  })

  test('US-15 when user clicks arrow next to relevance, it turns dark gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const relevanceScoreHeader = screen.getByText('Relevance Score');
      const sortButton = within(relevanceScoreHeader.closest('th')).getByRole('button');
      fireEvent.click(sortButton);
      expect(sortButton).toHaveClass('bg-gray-600');
    }, { timeout: 5000 });
  })

  // When user clicks on arrow next to date, results are sorted by date

  test('US-15 When user clicks on arrow next to date twice, results are sorted by date descending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const yearScoreHeader = screen.getByText('Year');
      sortButton = within(yearScoreHeader.closest('th')).getByRole('button');
    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("2024-07-01")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("2024-05-31")).toBeInTheDocument()
    }
    else
      fail('no sort button')

  })


  test('US-15 When user clicks on arrow next to date, results are sorted by date ascending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const yearScoreHeader = screen.getByText('Year');
      sortButton = within(yearScoreHeader.closest('th')).getByRole('button');

    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("2024-05-31")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("2024-07-01")).toBeInTheDocument()
    } else
      fail('no sort button found')
  })


  test('US-15 when results load date arrow is light gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const yearHeader = screen.getByText('Year');
      const sortButton = within(yearHeader.closest('th')).getByRole('button');
      expect(sortButton).toHaveClass('bg-gray-400');
    }, { timeout: 5000 });
  })

  test('US-15 When user clicks on arrow next to date, bg color turns dark gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const yearHeader = screen.getByText('Year');
      const sortButton = within(yearHeader.closest('th')).getByRole('button')
      fireEvent.click(sortButton);
      expect(sortButton).toHaveClass('bg-gray-600');
    }, { timeout: 5000 });
  })
  // When user clicks on arrow next to database, results are sorted by database


  test('US-15 When user clicks on arrow next to source twice, results are sorted by source descending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const sourceScoreHeader = screen.getByText('Source');
      sortButton = within(sourceScoreHeader.closest('th')).getByRole('button');
    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("Scopus")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("Science Direct")).toBeInTheDocument()
    }
    else
      fail('no sort button')

  })


  test('US-15 When user clicks on arrow next to source, results are sorted by source ascending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const sourceScoreHeader = screen.getByText('Source');
      sortButton = within(sourceScoreHeader.closest('th')).getByRole('button');

    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("Science Direct")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("Scopus")).toBeInTheDocument()
    } else
      fail('no sort button found')
  })


  test('US-15 when results load source arrow is light gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const sourceHeader = screen.getByText('Source');
      const sortButton = within(sourceHeader.closest('th')).getByRole('button');
      expect(sortButton).toHaveClass('bg-gray-400');
    }, { timeout: 5000 });
  })

  test('US-15 When user clicks on arrow next to source, bg color turns dark gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const sourceHeader = screen.getByText('Source');
      const sortButton = within(sourceHeader.closest('th')).getByRole('button')
      fireEvent.click(sortButton);
      expect(sortButton).toHaveClass('bg-gray-600');
    }, { timeout: 5000 });
  })


  test('US-15 When user clicks on arrow next to source,bg color turns dark gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const sourceHeader = screen.getByText('Source');
      const sortButton = within(sourceHeader.closest('th')).getByRole('button')
      fireEvent.click(sortButton);
      expect(sortButton).toHaveClass('bg-gray-600');
    }, { timeout: 5000 });
  })



  // When user clicks on arrow next to title, results are sorted by title

  test('US-15 When user clicks on arrow next to title twice, results are sorted by title descending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const titleScoreHeader = screen.getByText('Title');
      sortButton = within(titleScoreHeader.closest('th')).getByRole('button');
    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("test 2")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("test 1")).toBeInTheDocument()
    }
    else
      fail('no sort button')

  })


  test('US-15 When user clicks on arrow next to title, results are sorted by title ascending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const titleScoreHeader = screen.getByText('Title');
      sortButton = within(titleScoreHeader.closest('th')).getByRole('button');

    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("test 1")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("test 2")).toBeInTheDocument()
    } else
      fail('no sort button found')
  })

  test('US-15 when results load title arrow is light gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const titleHeader = screen.getByText('Title');
      const sortButton = within(titleHeader.closest('th')).getByRole('button');
      expect(sortButton).toHaveClass('bg-gray-400');
    }, { timeout: 5000 });
  })



  test('US-15 When user clicks on arrow next to title,bg color turns dark gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const titleHeader = screen.getByText('Title');
      const sortButton = within(titleHeader.closest('th')).getByRole('button')
      fireEvent.click(sortButton);
      expect(sortButton).toHaveClass('bg-gray-600');
    }, { timeout: 5000 });
  })

  // When user clicks on arrow next to color, results are sorted by color


  test('US-15 When user clicks on arrow next to Assessment twice, results are sorted by Assessment descending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const colorScoreHeader = screen.getByText('Assessment');
      sortButton = within(colorScoreHeader.closest('th')).getByRole('button');
    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("yellow")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("red")).toBeInTheDocument()
    }
    else
      fail('no sort button')

  })


  test('US-15 When user clicks on arrow next to color, results are sorted by color ascending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const colorScoreHeader = screen.getByText('Assessment');
      sortButton = within(colorScoreHeader.closest('th')).getByRole('button');

    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
      const rows = screen.getAllByTestId('row')
      expect(within(rows[0]).queryByText("red")).toBeInTheDocument()
      expect(within(rows[1]).queryByText("yellow")).toBeInTheDocument()
    } else
      fail('no sort button found')
  })


  test('US-15 when results load color arrow is light gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const colorHeader = screen.getByText('Assessment');
      const sortButton = within(colorHeader.closest('th')).getByRole('button');
      expect(sortButton).toHaveClass('bg-gray-400');
    }, { timeout: 5000 });
  })

  test('US-15 When user clicks on arrow next to color,bg color turns dark gray', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const colorHeader = screen.getByText('Assessment');
      const sortButton = within(colorHeader.closest('th')).getByRole('button')
      fireEvent.click(sortButton);
      expect(sortButton).toHaveClass('bg-gray-600');
    }, { timeout: 5000 });
  })

// When user clicks on arrow next to cited by, results are sorted by cited by


test('US-15 When user clicks on arrow next to citedby twice, results are sorted by citedby descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const citedbyScoreHeader = screen.getByText('Cited By');
    sortButton = within(citedbyScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[2].textContent).toBe("1");
    expect(rows[1].children[2].textContent).toBe("0");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to citedby, results are sorted by citedby ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const citedbyScoreHeader = screen.getByText('Cited By');
    sortButton = within(citedbyScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[2].textContent).toBe("0");
    expect(rows[1].children[2].textContent).toBe("1");

  } else
    fail('no sort button found')
})


test('US-15 when results load citedby arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const citedbyHeader = screen.getByText('Cited By');
    const sortButton = within(citedbyHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to citedby,bg citedby turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const citedbyHeader = screen.getByText('Cited By');
    const sortButton = within(citedbyHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})


// When user clicks on arrow next to URL, results are sorted by URL


test('US-15 When user clicks on arrow next to URL twice, results are sorted by URL descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const urlScoreHeader = screen.getByText('URL');
    sortButton = within(urlScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[3].textContent).toBe("link x");
    expect(rows[1].children[3].textContent).toBe("link a");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to url, results are sorted by url ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const urlScoreHeader = screen.getByText('URL');
    sortButton = within(urlScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[3].textContent).toBe("link a");
    expect(rows[1].children[3].textContent).toBe("link x");

  } else
    fail('no sort button found')
})


test('US-15 when results load url arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const urlHeader = screen.getByText('URL');
    const sortButton = within(urlHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to url,bg url turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const urlHeader = screen.getByText('URL');
    const sortButton = within(urlHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})


// When user clicks on arrow next to Abstract, results are sorted by Abstract


test('US-15 When user clicks on arrow next to abstract twice, results are sorted by abstract descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const abstractScoreHeader = screen.getByText('Abstract');
    sortButton = within(abstractScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[4].textContent).toBe("b");
    expect(rows[1].children[4].textContent).toBe("a");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to abstract, results are sorted by abstract ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const abstractScoreHeader = screen.getByText('Abstract');
    sortButton = within(abstractScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[4].textContent).toBe("a");
    expect(rows[1].children[4].textContent).toBe("b");

  } else
    fail('no sort button found')
})


test('US-15 when results load abstract arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const abstractHeader = screen.getByText('Abstract');
    const sortButton = within(abstractHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to abstract,bg abstract turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const abstractHeader = screen.getByText('Abstract');
    const sortButton = within(abstractHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})



// When user clicks on arrow next to doctype, results are sorted by doctype


test('US-15 When user clicks on arrow next to doctype twice, results are sorted by doctype descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const doctypeScoreHeader = screen.getByText('Document Type');
    sortButton = within(doctypeScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[5].textContent).toBe("journal");
    expect(rows[1].children[5].textContent).toBe("article");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to doctype, results are sorted by doctype ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const doctypeScoreHeader = screen.getByText('Document Type');
    sortButton = within(doctypeScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[5].textContent).toBe("article");
    expect(rows[1].children[5].textContent).toBe("journal");

  } else
    fail('no sort button found')
})


test('US-15 when results load doctype arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const doctypeHeader = screen.getByText('Document Type');
    const sortButton = within(doctypeHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to doctype,bg doctype turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const doctypeHeader = screen.getByText('Document Type');
    const sortButton = within(doctypeHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})



// When user clicks on arrow next to evaluationCritera, results are sorted by evaluationCritera


test('US-15 When user clicks on arrow next to evaluationCritera twice, results are sorted by evaluationCritera descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const evaluationCriteraScoreHeader = screen.getByText('Evaluation Criteria');
    sortButton = within(evaluationCriteraScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[7].textContent).toBe("deny");
    expect(rows[1].children[7].textContent).toBe("accept");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to evaluationCritera, results are sorted by evaluationCritera ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const evaluationCriteraScoreHeader = screen.getByText('Evaluation Criteria');
    sortButton = within(evaluationCriteraScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[7].textContent).toBe("accept");
    expect(rows[1].children[7].textContent).toBe("deny");

  } else
    fail('no sort button found')
})


test('US-15 when results load evaluationCritera arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const evaluationCriteraHeader = screen.getByText('Evaluation Criteria');
    const sortButton = within(evaluationCriteraHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to evaluationCritera,bg evaluationCritera turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const evaluationCriteraHeader = screen.getByText('Evaluation Criteria');
    const sortButton = within(evaluationCriteraHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})





// When user clicks on arrow next to methodology, results are sorted by methodology


test('US-15 When user clicks on arrow next to methodology twice, results are sorted by methodology descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const methodologyScoreHeader = screen.getByText('Methodology');
    sortButton = within(methodologyScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[10].textContent).toBe("1");
    expect(rows[1].children[10].textContent).toBe("0");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to methodology, results are sorted by methodology ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const methodologyScoreHeader = screen.getByText('Methodology');
    sortButton = within(methodologyScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[10].textContent).toBe("0");
    expect(rows[1].children[10].textContent).toBe("1");

  } else
    fail('no sort button found')
})


test('US-15 when results load methodology arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const methodologyHeader = screen.getByText('Methodology');
    const sortButton = within(methodologyHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to methodology,bg methodology turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const methodologyHeader = screen.getByText('Methodology');
    const sortButton = within(methodologyHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})






// When user clicks on arrow next to clarity, results are sorted by clarity


test('US-15 When user clicks on arrow next to clarity twice, results are sorted by clarity descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const clarityScoreHeader = screen.getByText('Clarity');
    sortButton = within(clarityScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[11].textContent).toBe("1");
    expect(rows[1].children[11].textContent).toBe("0");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to clarity, results are sorted by clarity ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const clarityScoreHeader = screen.getByText('Clarity');
    sortButton = within(clarityScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[11].textContent).toBe("0");
    expect(rows[1].children[11].textContent).toBe("1");

  } else
    fail('no sort button found')
})


test('US-15 when results load clarity arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const clarityHeader = screen.getByText('Clarity');
    const sortButton = within(clarityHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to clarity,bg clarity turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const clarityHeader = screen.getByText('Clarity');
    const sortButton = within(clarityHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})





// When user clicks on arrow next to completeness, results are sorted by completeness


test('US-15 When user clicks on arrow next to completeness twice, results are sorted by completeness descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const completenessScoreHeader = screen.getByText('Completeness');
    sortButton = within(completenessScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[11].textContent).toBe("1");
    expect(rows[1].children[11].textContent).toBe("0");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to completeness, results are sorted by completeness ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const completenessScoreHeader = screen.getByText('Completeness');
    sortButton = within(completenessScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[11].textContent).toBe("0");
    expect(rows[1].children[11].textContent).toBe("1");

  } else
    fail('no sort button found')
})


test('US-15 when results load completeness arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const completenessHeader = screen.getByText('Completeness');
    const sortButton = within(completenessHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to completeness,bg completeness turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const completenessHeader = screen.getByText('Completeness');
    const sortButton = within(completenessHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})





// When user clicks on arrow next to transparency, results are sorted by transparency


test('US-15 When user clicks on arrow next to transparency twice, results are sorted by transparency descending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const transparencyScoreHeader = screen.getByText('Transparency');
    sortButton = within(transparencyScoreHeader.closest('th')).getByRole('button');
  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[11].textContent).toBe("1");
    expect(rows[1].children[11].textContent).toBe("0");

  }
  else
    fail('no sort button')

})


test('US-15 When user clicks on arrow next to transparency, results are sorted by transparency ascending', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  let sortButton;
  await waitFor(() => {
    const transparencyScoreHeader = screen.getByText('Transparency');
    sortButton = within(transparencyScoreHeader.closest('th')).getByRole('button');

  }, { timeout: 5000 });
  if (sortButton) {
    fireEvent.click(sortButton);
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[11].textContent).toBe("0");
    expect(rows[1].children[11].textContent).toBe("1");

  } else
    fail('no sort button found')
})


test('US-15 when results load transparency arrow is light gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);

  await waitFor(() => {
    const transparencyHeader = screen.getByText('Transparency');
    const sortButton = within(transparencyHeader.closest('th')).getByRole('button');
    expect(sortButton).toHaveClass('bg-gray-400');
  }, { timeout: 5000 });
})

test('US-15 When user clicks on arrow next to transparency,bg transparency turns dark gray', async () => {
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const transparencyHeader = screen.getByText('Transparency');
    const sortButton = within(transparencyHeader.closest('th')).getByRole('button')
    fireEvent.click(sortButton);
    expect(sortButton).toHaveClass('bg-gray-600');
  }, { timeout: 5000 });
})

test('Check error is returned when search fails to fetch/backend down', async () => {
  global.fetch = jest.fn(() => Promise.reject(new Error('Fetch failed'))) as jest.Mock;
  render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

  const searchButton = screen.getByText('Search');
  const inputs = screen.getAllByRole('textbox');
  fireEvent.change(inputs[0], { target: { value: testInput } });
  fireEvent.click(searchButton);
  await waitFor(() => {
    const errorText = screen.getByText('Fetch failed');
    expect(errorText).toBeInTheDocument();
  }, { timeout: 5000 });
})

test('sort results ascending',  () => {
const sorted = sortResults(items, 'title', 'asc')
expect(sorted).toEqual(items)

  

})

test('sort results descending', () => {
  const sorted = sortResults(items, 'title', 'desc')
  console.log(items[1])
  expect(sorted).toEqual([items[0], items[1],items[2] ])
  
    
  
  })

  test('returns an empty array when sorting an empty array', () => {
    expect(sortResults([], 'title', 'asc')).toEqual([]);
});



});
