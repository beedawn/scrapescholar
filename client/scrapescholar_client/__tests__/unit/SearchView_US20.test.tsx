import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import apiCalls from '@/app/api/apiCalls';
import submitSearch from '../helperFunctions/submitSearch';
import itemsJson from '../mockData/ItemsTestJson';
import fetchMock, { setSimulateInsufficientStorage, setDeleteSearch } from '../helperFunctions/apiMock';
import UserManagement from '@/app/components/UserManagement/UserManagement';
import DeleteUserModal from '@/app/components/UserManagement/modal/DeleteUserModal';
beforeEach(() => {
    global.fetch = fetchMock;
});

afterEach(() => {
    jest.restoreAllMocks();
});


describe('SearchView US-17 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"


    //UT-20.1
    test('US-20 Settings Accordion Expands and shows API Keys, APIKey Modal opens and has correct values', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const settingsAccordian = screen.getByText('Settings');
        fireEvent.click(settingsAccordian);
        await waitFor(() => {
            const apiKeyLink = screen.getByText('API Keys');
            expect(apiKeyLink).toBeInTheDocument();
           fireEvent.click(apiKeyLink)
        }, { timeout: 5000 });

        await waitFor(()=>{
            const scopusInput = screen.getByTestId("scopus-api-input")
            const sciencedirectInput = screen.getByTestId("sciencedirect-api-input")
            const submitButton = screen.getByTestId("api-key-submit")
            expect(scopusInput).toBeInTheDocument();
            expect(sciencedirectInput).toBeInTheDocument();
            expect(submitButton).toBeInTheDocument();
            //cannot test valid api key as it is not available in our front end via environment variables, and putting it here would expose an api key
            //manually tested
    },{timeout:5000})
    })


     //UT-20.3
     test('US-20 Settings Accordion Expands and shows API Keys, enter bad API key scopus', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const settingsAccordian = screen.getByText('Settings');
        fireEvent.click(settingsAccordian);
        await waitFor(() => {
            const apiKeyLink = screen.getByText('API Keys');
            expect(apiKeyLink).toBeInTheDocument();
           fireEvent.click(apiKeyLink)
        }, { timeout: 5000 });

        await waitFor(()=>{
            const scopusInput = screen.getByTestId("scopus-api-input")
            const sciencedirectInput = screen.getByTestId("sciencedirect-api-input")
            const submitButton = screen.getByText("Submit")
            expect(scopusInput).toBeInTheDocument();
            expect(sciencedirectInput).toBeInTheDocument();
            expect(submitButton).toBeInTheDocument();
            fireEvent.change(scopusInput, { target: { value: "bad_api_key" } });
            fireEvent.click(submitButton)
        },{timeout:5000})
        screen.debug();
        await waitFor(()=>{
            const failureMsg = screen.getByTestId("api-failure");
            expect(failureMsg).toBeInTheDocument();

        },{timeout:5000})
    })
    test('US-20 Settings Accordion Expands and shows API Keys, enter bad API key sciencedirect', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const settingsAccordian = screen.getByText('Settings');
        fireEvent.click(settingsAccordian);
        await waitFor(() => {
            const apiKeyLink = screen.getByText('API Keys');
            expect(apiKeyLink).toBeInTheDocument();
           fireEvent.click(apiKeyLink)
        }, { timeout: 5000 });

        await waitFor(()=>{
            const scopusInput = screen.getByTestId("scopus-api-input")
            const sciencedirectInput = screen.getByTestId("sciencedirect-api-input")
            const submitButton = screen.getByText("Submit")
            expect(scopusInput).toBeInTheDocument();
            expect(sciencedirectInput).toBeInTheDocument();
            expect(submitButton).toBeInTheDocument();
            fireEvent.change(sciencedirectInput, { target: { value: "bad_api_key" } });
            fireEvent.click(submitButton)
        },{timeout:5000})
        await waitFor(()=>{
            const failureMsg = screen.getByTestId("api-failure");
            expect(failureMsg).toBeInTheDocument();

        },{timeout:5000})
    })
    test('US-20 Settings Accordion Expands and shows API Keys, enter bad API key sciencedirect and scopus', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const settingsAccordian = screen.getByText('Settings');
        fireEvent.click(settingsAccordian);
        await waitFor(() => {
            const apiKeyLink = screen.getByText('API Keys');
            expect(apiKeyLink).toBeInTheDocument();
           fireEvent.click(apiKeyLink)
        }, { timeout: 5000 });

        await waitFor(()=>{
            const scopusInput = screen.getByTestId("scopus-api-input")
            const sciencedirectInput = screen.getByTestId("sciencedirect-api-input")
            const submitButton = screen.getByText("Submit")
            expect(scopusInput).toBeInTheDocument();
            expect(sciencedirectInput).toBeInTheDocument();
            expect(submitButton).toBeInTheDocument();
            fireEvent.change(sciencedirectInput, { target: { value: "bad_api_key" } });
            fireEvent.change(scopusInput, { target: { value: "bad_api_key" } });
            fireEvent.click(submitButton)
        },{timeout:5000})
        await waitFor(()=>{
            const failureMsg = screen.getByTestId("api-failure");
            expect(failureMsg).toBeInTheDocument();

        },{timeout:5000})
    })


});
