import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';

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
            "methodology": "0",
            "clarity": "0",
            "transparency": "0",
            "completeness": "0"
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

  test('US-15 When user clicks on arrow next to source twice, results are sorted by source descending', async () => {
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


  test('US-15 When user clicks on arrow next to source, results are sorted by source ascending', async () => {
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


  test('US-15 When user clicks on arrow next to color twice, results are sorted by color descending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const colorScoreHeader = screen.getByText('Color');
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


  test('US-15 When user clicks on arrow next to source, results are sorted by source ascending', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);

    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let sortButton;
    await waitFor(() => {
      const colorScoreHeader = screen.getByText('Color');
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
      const colorHeader = screen.getByText('Color');
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
      const colorHeader = screen.getByText('Color');
      const sortButton = within(colorHeader.closest('th')).getByRole('button')
      fireEvent.click(sortButton);
      expect(sortButton).toHaveClass('bg-gray-600');
    }, { timeout: 5000 });
  })

});
