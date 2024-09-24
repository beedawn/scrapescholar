import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../../app/page';
import React from 'react';

describe('Home Component', () => {
  test('check login button loads', () => {
    render(<Home />);
    //finds + button
    const loginButton = screen.getByText('Login');
    expect(loginButton).toBeInTheDocument();
  });

  test('check login button click works', () => {
    render(<Home />);
    const loginButton = screen.getByText('Login');
    //clicks + button
    fireEvent.click(loginButton);
    //should be 2 inputs now
    expect(screen.getAllByRole('textbox')).toHaveLength(1);
    expect(screen.getByText('ScrapeScholar')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
    //maybe should test there are two + buttons too?
  });

  test('check logout button renders in SearchView', () => {
    render(<Home />);
    const loginButton = screen.getByText('Login');
    //clicks + button
    fireEvent.click(loginButton);
    //should be 2 inputs now
    const logoutButton = screen.getByText('Logout');
    expect(logoutButton).toBeInTheDocument();
  });

  test('check logout button works in SearchView', () => {
    render(<Home />);
    const loginButton = screen.getByText('Login');
    //clicks + button
    fireEvent.click(loginButton);
    //should be 2 inputs now
    const logoutButton = screen.getByText('Logout');
    expect(logoutButton).toBeInTheDocument();
    fireEvent.click(logoutButton);
    const loginButton2 = screen.getByText('Login');
    expect(loginButton2).toBeInTheDocument();
  });

});
