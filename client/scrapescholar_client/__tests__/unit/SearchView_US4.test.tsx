import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';

import submitSearch from '../helperFunctions/submitSearch';
import itemsJson from '../mockData/ItemsTestJson';
import fetchMock, { setSimulateInsufficientStorage, setDeleteSearch } from '../helperFunctions/apiMock';

beforeEach(() => {
    global.fetch = fetchMock;
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

    test('US-4 pencil is next to value in search title', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            const searchTitleDiv = screen.getByTestId('search-title')
            expect(searchTitleDiv.textContent).toContain("✎");
        }, { timeout: 5000 });
    })

    test('US-4 When user clicks on pencil next to search title, text field turns into input box', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            const pencilIcons = screen.getAllByText("✎");
            fireEvent.click(pencilIcons[0]);
            const searchTitleDiv = screen.getByTestId('search-title')
            const input = searchTitleDiv.querySelector('input');
            expect(input).toBeInTheDocument();
        }, { timeout: 5000 });
    })

    test('US-4 When user clicks on pencil next to search title, text field turns into input box, then x button is pressed and reverts back to plain text', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            const pencilIcons = screen.getAllByText("✎");
            fireEvent.click(pencilIcons[0]);
            const closeIcons = screen.getAllByText("×");
            fireEvent.click(closeIcons[0]);
            const searchTitleDiv = screen.getByTestId('search-title')
            const span = searchTitleDiv.querySelector('span');
            expect(span).toBeInTheDocument();
        }, { timeout: 5000 });
    })

    test('US-4 When user clicks on pencil next to search title, text field turns into input box, then check button is pressed and reverts back to new text', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        let searchTitleDiv: Element | null = null;
        await waitFor(() => {
            const pencilIcons = screen.getAllByText("✎");
            fireEvent.click(pencilIcons[0]);
            searchTitleDiv = screen.getByTestId('search-title')
            const input = searchTitleDiv.querySelector('input');
            if (input) {
                fireEvent.change(input, { target: { value: "test 1" } });
                
                const checkIcons = screen.getAllByText("✔");
                fireEvent.click(checkIcons[0]);
            }
            else {
                fail('no input found after clicking pencil')
            }
        }, { timeout: 5000 });
        const searchTitleSpan = screen.getByTestId('search-title-span')
     
        if (searchTitleDiv)
            
            expect(searchTitleSpan.textContent).toContain("test 1");
        else {
            fail('no input found after clicking pencil')
        }


    })

    test('US-4  Past search dropdown should be visable', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        //submitSearch(testInput);
        await waitFor(() => {
            const pastDropdown = screen.getAllByRole('combobox');

            fireEvent.click(pastDropdown[0]);
            expect(pastDropdown[0]).toBeInTheDocument();

        }, { timeout: 5000 });
       
    

        
    })
    test('US-4  Past search dropdown should contain a search', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        //submitSearch(testInput);
        await waitFor(() => {
            const pastDropdown = screen.getAllByRole('combobox');

            fireEvent.click(pastDropdown[0]);
           
            

        }, { timeout: 5000 });
        const dropdownSearch = await screen.findByText('test dropdown');

        expect(dropdownSearch).toBeInTheDocument();
    

        
    })

    test('US-4  Past search dropdown should load a search', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        const pastDropdown = screen.getAllByRole('combobox');
        fireEvent.click(pastDropdown[0]);
        const dropdownSearch = await screen.findByText('test dropdown');
        fireEvent.change(pastDropdown[0], { target: { value: '1' } });

        const title =/Law and war in the virtual era/i;
        const link= /https\:\/\/www.scopus.com\/inward\/record.uri\?partnerID\=HzOxMe3b\&scp\=70649105643\&origin\=inward/i;
        const date= /2009\-01\-01/i;
        const document_type=/Article/i;

        await waitFor(async () => {
            expect(await screen.findByText(title)).toBeInTheDocument();
            expect(await screen.findByText(link)).toBeInTheDocument();
            expect(await screen.findByText(date)).toBeInTheDocument();
            expect(await screen.findByText(document_type)).toBeInTheDocument();
        }, { timeout: 5000 });
    })

    test('US-4  When user hits 300 searches and submits a search data deletion screen should be displayed', async () => {
        setSimulateInsufficientStorage(true);
         
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  
        submitSearch(testInput);
   
        await waitFor(async () => {
             const dataMessage = /SearchData is Full\!/i
             const dataMsg = await screen.findByText(dataMessage)
            expect(dataMsg).toBeInTheDocument();
         
        }, { timeout: 10000 });
        setSimulateInsufficientStorage(false);
    })

    test('US-4  When user hits 300 searches and submits multiple search requests data deletion screen should be displayed', async () => {
        setSimulateInsufficientStorage(true);
         
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  
        submitSearch(testInput);
        submitSearch(testInput);
   
        await waitFor(async () => {
             const dataMessage = /SearchData is Full\!/i
             const dataMsg = await screen.findByText(dataMessage)
            expect(dataMsg).toBeInTheDocument();
           
        }, { timeout: 10000 });
        setSimulateInsufficientStorage(false);
    })

    test('US-4  When user hits 300 searches and submits a search, then deletes a search, they should be able to submit another search', async () => {
        setSimulateInsufficientStorage(true);
         
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
  
        submitSearch(testInput);
        submitSearch(testInput);
   
        await waitFor(async () => {
             const dataMessage = /SearchData is Full\!/i
             const dataMsg = await screen.findByText(dataMessage)
            expect(dataMsg).toBeInTheDocument();
           
        }, { timeout: 5000 });
        setDeleteSearch(true);
        submitSearch(testInput);


        await waitFor(async () => {
            const dataMessage = /SearchData is Full\!/i
            const dataMsg = screen.queryByText(dataMessage)
            expect(dataMsg).toBeNull()
         
       }, { timeout: 5000 });
      
       setDeleteSearch(false);
        setSimulateInsufficientStorage(false);
    })



   
});
