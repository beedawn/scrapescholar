import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView  from '../../app/views/SearchView';
import React from 'react';
import fetchMock from '../helperFunctions/apiMock';


beforeEach(() => {
    global.fetch = fetchMock;
    });

afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView AR-6 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"
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

});
