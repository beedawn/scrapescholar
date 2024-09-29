import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, { ResultItem } from '../../app/views/SearchView';
import React from 'react';
import fetchMock from '../helperFunctions/apiMock';



beforeEach(() => {
    global.fetch = fetchMock;
  });
afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView US-15 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"

  //US-15 When user clicks on arrow next to relevance, results are sorted by relevance
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
      expect(rows[0].children[2].textContent).toContain("1");
      expect(rows[1].children[2].textContent).toContain("0");
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
      expect(rows[0].children[2].textContent).toContain("0");
      expect(rows[1].children[2].textContent).toContain("1");
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
      expect(rows[0].children[3].textContent).toContain("link x");
      expect(rows[1].children[3].textContent).toContain("link a");
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
      expect(rows[0].children[3].textContent).toContain("link a");
      expect(rows[1].children[3].textContent).toContain("link x");
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
      expect(rows[0].children[4].textContent).toContain("b");
      expect(rows[1].children[4].textContent).toContain("a");
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
      expect(rows[0].children[4].textContent).toContain("a");
      expect(rows[1].children[4].textContent).toContain("b");
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
      expect(rows[0].children[5].textContent).toContain("journal");
      expect(rows[1].children[5].textContent).toContain("article");
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
      expect(rows[0].children[5].textContent).toContain("article");
      expect(rows[1].children[5].textContent).toContain("journal");
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
      expect(rows[0].children[7].textContent).toContain("deny");
      expect(rows[1].children[7].textContent).toContain("accept");
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
      expect(rows[0].children[7].textContent).toContain("accept");
      expect(rows[1].children[7].textContent).toContain("deny");
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
      expect(rows[0].children[10].textContent).toContain("1");
      expect(rows[1].children[10].textContent).toContain("0");
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
      expect(rows[0].children[10].textContent).toContain("0");
      expect(rows[1].children[10].textContent).toContain("1");
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
      expect(rows[0].children[11].textContent).toContain("1");
      expect(rows[1].children[11].textContent).toContain("0");
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
      expect(rows[0].children[11].textContent).toContain("0");
      expect(rows[1].children[11].textContent).toContain("1");
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
      expect(rows[0].children[12].textContent).toContain("1");
      expect(rows[1].children[12].textContent).toContain("0");
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
      expect(rows[0].children[12].textContent).toContain("0");
      expect(rows[1].children[12].textContent).toContain("1");
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
      expect(rows[0].children[13].textContent).toContain("1");
      expect(rows[1].children[13].textContent).toContain("0");
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
      expect(rows[0].children[13].textContent).toContain("0");
      expect(rows[1].children[13].textContent).toContain("1");
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

  test('US-15 When user clicks on arrow next to title,bg color turns dark gray, then clicks on color arrow, and title should be light grey', async () => {
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
      const yearHeader = screen.getByText('Year');
      const sortButton2 = within(yearHeader.closest('th')).getByRole('button')
      fireEvent.click(sortButton2);
      expect(sortButton2).toHaveClass('bg-gray-600');
      expect(sortButton).toHaveClass('bg-gray-400');
    }, { timeout: 5000 });
  })

});
