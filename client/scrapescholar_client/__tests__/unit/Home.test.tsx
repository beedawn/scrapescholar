import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../../app/page';
import React from 'react';



describe('Home Component', () => {

  const admin_user = process.env.NEXT_PUBLIC_ADMIN_USER;
  const admin_pass = process.env.NEXT_PUBLIC_ADMIN_PASS;
  test('check login button loads', () => {
    render(<Home />);
    //finds + button
    const loginButton = screen.getByText('Login');
    expect(loginButton).toBeInTheDocument();
  });

  test('check login button click works', () => {
    render(<Home />);


   
    //clicks + button

    const usernameInput = screen.getByPlaceholderText('Username');
    const passwordInput = screen.getByPlaceholderText('Password');
    fireEvent.change(usernameInput, { target: { value: admin_user } });
    fireEvent.change(passwordInput, { target: { value: admin_pass } });
    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);
    //should be 2 inputs now
    expect(screen.getAllByRole('textbox')).toHaveLength(1);
    expect(screen.getByText('ScrapeScholar')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
    //maybe should test there are two + buttons too?
  });


  test('US-4 check logout button works in SearchView', async () => {
    render(<Home />);
    const usernameInput = screen.getByPlaceholderText('Username');
    const passwordInput = screen.getByPlaceholderText('Password');
    fireEvent.change(usernameInput, { target: { value: admin_user } });
    fireEvent.change(passwordInput, { target: { value: admin_pass } });
    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);


    await waitFor(() => {

   
    const logoutButton = screen.getByText('Logout');
    expect(logoutButton).toBeInTheDocument();
    fireEvent.click(logoutButton);
  }, { timeout: 5000 });
  await waitFor(() => {
    const loginButton2 = screen.getByText('Login');
    expect(loginButton2).toBeInTheDocument();
  }, { timeout: 5000 });
  });

  test('US-4 check login button click denies empty credetials', () => {
    render(<Home />);
    const loginButton = screen.getByText('Login');
    //clicks + button
    fireEvent.click(loginButton);
    //should be 2 inputs now
   
    expect(screen.getByText('Invalid Login')).toBeInTheDocument();
    //maybe should test there are two + buttons too?
  });




});
