import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';
import submitSearch from '../helperFunctions/submitSearch';
import accordianContainsSources from '../helperFunctions/accordianContainsSources';
import apiCalls from '@/app/api/apiCalls';

describe('Home Component', () => {
  const admin_user = process.env.NEXT_PUBLIC_ADMIN_USER|| "";
  const admin_pass = process.env.NEXT_PUBLIC_ADMIN_PASS||"";

  beforeEach(async () => {

    const { postAPILogin } = apiCalls();
    // Set cookie manually before running the test
    const tokenResponse=await postAPILogin(admin_user, admin_pass);
        
    document.cookie = `access_token=${tokenResponse}; path=/;`;
  });
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"












});
