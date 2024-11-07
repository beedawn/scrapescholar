import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import apiCalls from '@/app/api/apiCalls';
import submitSearch from '../helperFunctions/submitSearch';
import itemsJson from '../mockData/ItemsTestJson';
import fetchMock, { setSimulateInsufficientStorage, setDeleteSearch } from '../helperFunctions/apiMock';
import UserManagement from '@/app/components/UserManagement/UserManagement';
beforeEach(() => {
    global.fetch = fetchMock;
});

afterEach(() => {
    jest.restoreAllMocks();
});


describe('SearchView US-17 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"

//UT-25.1
    // test('US-5 UT-5.1 check relevancy column contains %', () => {
    //     render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    //     submitSearch(testInput)

    //     waitFor(() => {
    //         const rows = screen.getAllByTestId('row')
    //         expect(rows[0].children[9].textContent).toContain(/92/i);
    //         expect(rows[0].children[9].textContent).toContain(/%/i);
    //     }, { timeout: 5000 })
    // });

    test('US-17 Settings Accordion Expands and shows API Keys', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const settingsAccordian = screen.getByText('Settings');
        fireEvent.click(settingsAccordian);
        await waitFor(() => {
            const apiKeyLink = screen.getByText('API Keys');
            expect(apiKeyLink).toBeInTheDocument();
        }, { timeout: 5000 });

    })


    test('US-17 Settings Accordion Expands and changes classes on mouseover', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const settingsAccordian = screen.getByText('Settings');
        fireEvent.click(settingsAccordian);
        await waitFor(() => {
            const apiKeyLink = screen.getByText('API Keys');
            fireEvent.mouseOver(apiKeyLink)
            expect(apiKeyLink).toHaveClass("text-blue-200 underline")
        }, { timeout: 5000 });

    })


    test('US-17 Settings Accordion Expands and changes classes on mouseout', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const settingsAccordian = screen.getByText('Settings');
        fireEvent.click(settingsAccordian);
        await waitFor(() => {
            const apiKeyLink = screen.getByText('API Keys');
            fireEvent.mouseOver(apiKeyLink)
            fireEvent.mouseOut(apiKeyLink)
            expect(apiKeyLink).toHaveClass("text-blue-400 underline")
        }, { timeout: 5000 });

    })

    test('US-17 Make sure Usermanagement has New User Button and New User Modal works and has text and fields', async () => {
        render(<UserManagement />);
        const newUserButton = screen.getByText('New User');
        expect(newUserButton).toBeInTheDocument()
        fireEvent.click(newUserButton)
        waitFor(()=>{
            const username_text = screen.getByText("Username")
            const password_text = screen.getByText("Password")
            const email_text = screen.getByText("Email")
            expect(username_text).toBeInTheDocument();
            expect(password_text).toBeInTheDocument();
            expect(email_text).toBeInTheDocument();
            const username_input = screen.getByPlaceholderText("Username");
            const password_input = screen.getByPlaceholderText("Password");
            const email_input = screen.getAllByPlaceholderText("Email");
            expect(username_input).toBeInTheDocument();
            expect(password_input).toBeInTheDocument();
            expect(email_input).toBeInTheDocument();

        },{timeout:5000})

    })

    test('US-17 Make sure Usermanagement has New User Button and New User Modal works and closes', async () => {
        render(<UserManagement />);
        const newUserButton = screen.getByText('New User');
        expect(newUserButton).toBeInTheDocument()
        fireEvent.click(newUserButton)
        waitFor(()=>{
            const closeButton= screen.getByText("Close")
            fireEvent.click(closeButton)


            const username_text = screen.getByText("Username")
            const password_text = screen.getByText("Password")
            const email_text = screen.getByText("Email")
            expect(username_text).not.toBeInTheDocument();
            expect(password_text).not.toBeInTheDocument();
            expect(email_text).not.toBeInTheDocument();
            const username_input = screen.getByPlaceholderText("Username");
            const password_input = screen.getByPlaceholderText("Password");
            const email_input = screen.getAllByPlaceholderText("Email");
            expect(username_input).not.toBeInTheDocument();
            expect(password_input).not.toBeInTheDocument();
            expect(email_input).not.toBeInTheDocument();

        },{timeout:5000})

    })


    test('US-17 Make sure Usermanagement has New User Button and New User Modal works and inputs work', async () => {
        render(<UserManagement />);
        const newUserButton = screen.getByText('New User');
        expect(newUserButton).toBeInTheDocument()
        fireEvent.click(newUserButton)
        waitFor(()=>{
     


            const username_input = screen.getByPlaceholderText("Username");
            const password_input = screen.getByPlaceholderText("Password");
            const email_input = screen.getAllByPlaceholderText("Email");
            fireEvent.change(username_input, { target: { value: 'test_user' } });
            fireEvent.change(password_input, { target: { value: 'test' } });
            const password_msg = screen.getByText("Password must be at least 8 characters long")
            expect(password_msg).toBeInTheDocument();
            fireEvent.change(password_input, { target: { value: 'testtest' } });
            const password_msg2 = screen.getByText("Password must be at least 8 characters long")
            expect(password_msg2).not.toBeInTheDocument();

            const submitButton = screen.getByText("Submit");
            fireEvent.click(submitButton);
            const error_msg = screen.getByText("Error, please try again.");
            expect(error_msg).toBeInTheDocument();

            fireEvent.change(password_input, { target: { value: 'testtest' } });
            const error_msg2 = screen.getByText("Error, please try again.");
            expect(error_msg2).not.toBeInTheDocument();
            const submitButton2 = screen.getByText("Submit");
            fireEvent.click(submitButton2);
            const error_msg3 = screen.getByText("Error, please try again.");
            expect(error_msg3).toBeInTheDocument();
            fireEvent.click(password_input)
            expect(error_msg3).toBeInTheDocument();
            const dropdown = screen.getByText('Role');
            fireEvent.change(dropdown, { target: { value: 'GradStudent' } });
            expect(dropdown).toBeInTheDocument();
            expect(dropdown.value).toBe('GradStudent');


        },{timeout:5000})

    })
});
