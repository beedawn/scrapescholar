import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../../app/page';
import React from 'react';

describe('Home Component', () => {

  const admin_user = process.env.NEXT_PUBLIC_ADMIN_USER;
  const admin_pass = process.env.NEXT_PUBLIC_ADMIN_PASS;

  test('US-4 check login button loads', () => {
    render(<Home />);
    waitFor(()=>{
    const loginButton = screen.getByText('Login');
    expect(loginButton).toBeInTheDocument();
  },{timeout:5000})
  });

  test('US-4 check username field is on page', async () => {
    render(<Home />);
    waitFor(()=>{
    const usernameInput = screen.getByPlaceholderText('Username');
    expect(usernameInput).toBeInTheDocument();
    },{timeout:5000})
  });

  test('US-4 check password field is on page', async () => {
    render(<Home />);
   await waitFor(()=>{
    const passwordInput = screen.getByPlaceholderText('Password');
    expect(passwordInput).toBeInTheDocument();
    },{timeout:5000})
  });

  test('check login button click works', async () => {
    render(<Home />);
    await waitFor(()=>{
    const usernameInput = screen.getByPlaceholderText('Username');
    const passwordInput = screen.getByPlaceholderText('Password');
    fireEvent.change(usernameInput, { target: { value: admin_user } });
    fireEvent.change(passwordInput, { target: { value: admin_pass } });
    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);
  },{timeout:5000})
    await waitFor(() => {
      expect(screen.getAllByRole('textbox')).toHaveLength(1);
      expect(screen.getByText('ScrapeScholar')).toBeInTheDocument();
      expect(screen.getByText('Search')).toBeInTheDocument();
    }, { timeout: 10000 });
  });

  test('US-4 check logout button works in SearchView', async () => {
    render(<Home />);
    waitFor(()=>{
    const usernameInput = screen.getByPlaceholderText('Username');
    const passwordInput = screen.getByPlaceholderText('Password');
    fireEvent.change(usernameInput, { target: { value: admin_user } });
    fireEvent.change(passwordInput, { target: { value: admin_pass } });
    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);
  },{timeout:5000})
    await waitFor(() => {
      const logoutButton = screen.getByText('Logout');
      expect(logoutButton).toBeInTheDocument();
      fireEvent.click(logoutButton);
    }, { timeout: 10000 });
    await waitFor(() => {
      const loginButton2 = screen.getByText('Login');
      expect(loginButton2).toBeInTheDocument();
    }, { timeout: 10000 });
  });

  test('US-4 check login button click denies empty credentials', async () => {
    render(<Home />);

    await waitFor(() => {
    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);
  }, { timeout: 10000 });

  screen.debug(undefined,10000);
    await waitFor(() => {
      expect(screen.getByText('Invalid Login')).toBeInTheDocument();
    }, { timeout: 10000 });

  });

});
