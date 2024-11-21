import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import fetchMock from '../helperFunctions/apiMock';
import submitSearch from '../helperFunctions/submitSearch';


beforeEach(() => {
    global.fetch = fetchMock;

    window.innerWidth = 375; //  mobile width
    window.innerHeight = 667; //  mobile height
    window.dispatchEvent(new Event('resize'));
});

afterEach(() => {
    jest.restoreAllMocks();
});


const clickTheBurger = () => {
    const hamburgerIcon = screen.getByTestId('hamburger_icon')
    fireEvent.click(hamburgerIcon)
}
describe('SearchView AR-2 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"
    //ARUT-2.1
    test('AR-2 hamburger is in UI', async () => {

        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        await waitFor(() => {
            const hamburgerIcon = screen.getByTestId('hamburger_icon')
            expect(hamburgerIcon).toBeInTheDocument()
        }, { timeout: 5000 });
        await waitFor(() => {

            clickTheBurger();
        }, { timeout: 5000 })
        await waitFor(() => {
            const navbar = screen.getByTestId('navbar')
            expect(navbar).toBeInTheDocument()
        })
        await waitFor(() => {
            const closeButton = screen.getByTestId('nav_close_button')
            fireEvent.click(closeButton)
        }, { timeout: 5000 })

        const navbar = screen.queryByTestId('navbar')
        expect(navbar).not.toBeInTheDocument()
        const menuBar = screen.getByTestId('menu_bar')
        expect(menuBar).toBeInTheDocument()


    })

    //ARUT-2.2
    test('AR-2 comments button generates', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        clickTheBurger()
        submitSearch(testInput);
        await waitFor(() => {
            const rows = screen.getAllByTestId('row');
            fireEvent.click(rows[0]);
        }, { timeout: 5000 });
        await waitFor(() => {
            const commentButton = screen.getByTestId("mobile_comments_button");
            expect(commentButton).toBeInTheDocument();
            fireEvent.click(commentButton);
        })
        await waitFor(() => {
            const commentsSideBar = screen.getByTestId("comments_sidebar");
            expect(commentsSideBar).toBeInTheDocument();
            const commentsSideBarClose = screen.getByTestId("comments_sidebar_close");
            fireEvent.click(commentsSideBarClose)
        }, { timeout: 5000 })

        await waitFor(() => {
            const commentButton = screen.getByTestId("mobile_comments_button");
            expect(commentButton).toBeInTheDocument();
        }, { timeout: 5000 })
    })

    //ARUT-2.3
    test('AR-2 scroll buttons in UI', async () => {

        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        clickTheBurger()
        submitSearch(testInput);
        await waitFor(() => {
            const leftScroll = screen.getByTestId('scroll_left');
            const rightScroll = screen.getByTestId('scroll_right');
            expect(leftScroll).toBeInTheDocument();
            expect(rightScroll).toBeInTheDocument();
        }, { timeout: 5000 });
    })
});
