import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
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

describe('SearchView AR-4 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"

    test('AR-4 pencil is next to value in methodology', async () => {
        
        act(()=>{render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);})
        screen.debug(undefined,100000);
        await waitFor(() => {
            const rows = screen.getAllByTestId('row')
            expect(rows[0].children[10].textContent).toContain("✎");
            expect(rows[1].children[10].textContent).toContain("✎");
        }, { timeout: 10000 });
        
    })

    test('AR-4 When user clicks on pencil next to value, text field turns into input box', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
     
        submitSearch(testInput);
        await waitFor(() => {
            const pencilIcons = screen.getAllByText("✎");
            fireEvent.click(pencilIcons[1]);
            const rows = screen.getAllByTestId('row');
            const methodologyField = rows[0].children[10];
            const input = methodologyField.querySelector('input');
            expect(input).toBeInTheDocument();
        }, { timeout: 5000 });
    })

    test('AR-4 When user clicks on pencil next to value, text field turns into input box, then x button is pressed and reverts back to plain text', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);

        await waitFor(() => {
            const pencilIcons = screen.getAllByText("✎");
            fireEvent.click(pencilIcons[1]);
            const closeIcons = screen.getAllByText("×");
            fireEvent.click(closeIcons[0]);
            const rows = screen.getAllByTestId('row');
            const methodologyField = rows[0].children[10];
            expect(methodologyField.textContent).toContain("0");
        }, { timeout: 5000 });
    })

    test('AR-4 When user clicks on pencil next to value, text field turns into input box, then check button is pressed and reverts back to new text', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        let methodologyField: Element | null = null;
        await waitFor(() => {
            const pencilIcons = screen.getAllByText("✎");
            fireEvent.click(pencilIcons[1]);
            const rows = screen.getAllByTestId('row');
            methodologyField = rows[0].children[10];
            const input = methodologyField.querySelector('input');
            if (input) {
                fireEvent.change(input, { target: { value: testInput } });
                const checkIcons = screen.getAllByText("✔");
                fireEvent.click(checkIcons[0]);
            }
            else {
                fail('no input found after clicking pencil')
            }

        }, { timeout: 5000 });
        if (methodologyField)
            expect(methodologyField.textContent).toContain(testInput);
        else {
            fail('no input found after clicking pencil')
        }
    })

    test('AR-4 When user clicks on pencil next to value, text field turns into input box, then check button is pressed and reverts back to new text after being sorted', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        let methodologyField: Element | null = null;
        let methodologyField2: Element | null = null;
        let sortButton;
        await waitFor(() => {
            const transparencyScoreHeader = screen.getByText('Transparency');
            sortButton = within(transparencyScoreHeader.closest('th')).getByRole('button');
        }, { timeout: 5000 });
        if (sortButton) {
            fireEvent.click(sortButton);
        } else
            fail('no sort button found')
        await waitFor(() => {
            const pencilIcons = screen.getAllByText("✎");
            fireEvent.click(pencilIcons[1]);
            fireEvent.click(pencilIcons[5]);
            const rows = screen.getAllByTestId('row');
            methodologyField = rows[0].children[10];
            const input = methodologyField.querySelector('input');
            methodologyField2 = rows[1].children[10];
            const input2 = methodologyField2.querySelector('input');
            if (input && input2) {
                fireEvent.change(input, { target: { value: testInput + "1" } });
                fireEvent.change(input2, { target: { value: testInput + "2" } });
                const checkIcons = screen.getAllByText("✔");
                fireEvent.click(checkIcons[0]);
                fireEvent.click(checkIcons[1]);
            }
            else {
                fail('no input found after clicking pencil')
            }
        }, { timeout: 5000 });

        if (methodologyField && methodologyField2) {
            const rows = screen.getAllByTestId('row');
            expect(rows[0].children[10].textContent).toContain("test input1");
            expect(rows[1].children[10].textContent).toContain("test input2");
        }
        else {
            fail('no input found after clicking pencil')
        }
    })

});
