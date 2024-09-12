import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

afterEach(async () => {
  // Sleep for 1 second after each test
  await sleep(1000);
});

describe('Home Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"
  test('check + button loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
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
    render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
    //checks how many input boxes there are 
    expect(screen.getAllByRole('textbox')).toHaveLength(1);
  });

  test('check - button loads', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton)
    //finds - button
    const deleteButton = screen.getByText('-');
    expect(deleteButton).toBeInTheDocument();
  });

  test('adds new input field on "+" button click', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
    const addButton = screen.getByText('+');
    //clicks + button
    fireEvent.click(addButton);
    //should be 2 inputs now
    expect(screen.getAllByRole('textbox')).toHaveLength(2);
    //maybe should test there are two + buttons too?
  });

  test('updates input value correctly', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    expect(inputs[0]).toHaveValue(testInput);
  });


  test('shows No results found after search press', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true}/>);
    const searchButton = screen.getByText('Search');
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    fireEvent.click(addButton);
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: "abcdefg" } });
    fireEvent.change(inputs[1], { target: { value: "hijklmnop" } });
    fireEvent.change(inputs[2], { target: { value: "12345678" } });
    fireEvent.click(searchButton);
    const expectedText = "No results found";
    await waitFor(()=>{
      expect(screen.getByText(new RegExp(expectedText,'i') )).toBeInTheDocument()
    }, {timeout: 5000});
  })

  test('shows you searched test input after search press', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true}/>);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    const expectedText = 'You searched ' + testInput;
    await waitFor(()=>{
      expect(screen.getByText(new RegExp(expectedText,'i') )).toBeInTheDocument()
    }, {timeout: 5000});
  })

  test('removes input when delete button clicked', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
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
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true}/>);
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
   render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    await waitFor(()=>{
      expect(screen.getByText('Please enter a keyword')).toBeInTheDocument();
    });
  });

  test('2 inputs with text in first field displays and/or dropdown', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn}/>);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput+" 2" } });
    const andDropdown = screen.getByDisplayValue('AND');
    expect(andDropdown).toBeInTheDocument();
  });

  test('and shows in results after search submitted', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true}/>);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput+" 2" } });
    const andDropdown = screen.getByDisplayValue('AND');
    expect(andDropdown).toBeInTheDocument();
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    const expectedText = 'You searched ' + testInput+ ' AND '+testInput+' 2';
    await waitFor(()=>{
      expect(screen.getByText(new RegExp(expectedText,'i') )).toBeInTheDocument()
      // expect(screen.getByText('You searched ' + testInput+ ' AND '+testInput+' 2')).toBeInTheDocument()
    }, { timeout: 5000 });
  });

  test('or shows in results after search submitted', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true}/>);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput+" 2" } });
    const dropdown = screen.getByDisplayValue('AND');
    // Simulate selecting the second option (OR)
    fireEvent.change(dropdown, { target: { value: Dropdown.OR } });
    expect(dropdown).toBeInTheDocument();
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    const expectedText = 'You searched ' + testInput+ ' OR '+testInput+' 2';
    await waitFor(()=>{
      expect(screen.getByText(new RegExp(expectedText,'i') )).toBeInTheDocument()
      // expect(screen.getByText('You searched ' + testInput+ ' OR '+testInput+' 2')).toBeInTheDocument()
    },{ timeout: 5000 });
  });

  test('not shows in results after search submitted', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true}/>);
    const addButton = screen.getByText('+');
    fireEvent.click(addButton);
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.change(inputs[1], { target: { value: testInput+" 2" } });
    const dropdown = screen.getByDisplayValue('AND');
    // Simulate selecting the second option (OR)
    fireEvent.change(dropdown, { target: { value: Dropdown.NOT } });
    expect(dropdown).toBeInTheDocument();
    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);
    await waitFor(()=>{expect(screen.getByText('You searched ' + testInput+ ' NOT '+testInput+' 2')).toBeInTheDocument()
    }, { timeout: 5000 })
  }, );
});
