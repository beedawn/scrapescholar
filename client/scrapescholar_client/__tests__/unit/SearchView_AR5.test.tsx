import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../../app/page';
import React from 'react';

describe('SearchView AR-5 Component', () => {

//AR-5.1
  test('UR-5 check azure login button loads', () => {
    render(<Home />);
    waitFor(()=>{
    const azureLoginButton = screen.getByText('Sign in with Azure AD');
    expect(azureLoginButton).toBeInTheDocument();
  },{timeout:5000})
  });

//AR-5.2
  test('UR-5 check azure login button loads microsoft page when clicked', () => {
    render(<Home />);
    waitFor(()=>{
    const azureLoginButton = screen.getByText('Sign in with Azure AD');
    expect(azureLoginButton).toBeInTheDocument();
    fireEvent.click(azureLoginButton)
  },{timeout:5000})
  waitFor(()=>{
    expect(global.window.location.pathname).toContain('microsoft');

  },{timeout:5000})
  });


});
