import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import CommentsSidebar from '../../app/components/SearchView/CommentsSidebar';
import React from 'react';
import apiCalls from '../../app/api/apiCalls';
import fetchMock from '../helperFunctions/apiMock';

jest.mock('../../app/api/apiCalls');

const mockApiCalls = apiCalls as jest.Mocked<typeof apiCalls>;

// Set global fetch to use fetchMock
global.fetch = fetchMock;

const mockAddComment = jest.fn();
const mockGetCommentsByArticle = jest.fn();
const mockEditComment = jest.fn();
const mockDeleteComment = jest.fn();

mockApiCalls.mockReturnValue({
    getCommentsByArticle: mockGetCommentsByArticle,
    addComment: mockAddComment,
    editComment: mockEditComment,
    deleteComment: mockDeleteComment,
});

describe('CommentsSidebar Component - UT-9.3 and UT-9.4', () => {
    const testArticleId = 1;
    const initialComment = { comment_id: 1, user_id: 123, comment_text: "Initial Comment" };

    beforeEach(() => {
        mockGetCommentsByArticle.mockResolvedValueOnce([initialComment]);
        mockAddComment.mockResolvedValueOnce({ comment_id: 2, user_id: 456, comment_text: "New Comment" });
        mockEditComment.mockResolvedValueOnce({ ...initialComment, comment_text: "Edited Comment" });
        mockDeleteComment.mockResolvedValueOnce({});
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test('UT-9.3: displays add comment interface and submits a new comment', async () => {
        await act(async () => {
            render(<CommentsSidebar articleId={testArticleId} onClose={jest.fn()} />);
        });

        await waitFor(() => expect(screen.getByPlaceholderText('Add a comment')).toBeInTheDocument());
        const addButton = screen.getByText('Add Comment');
        expect(addButton).toBeInTheDocument();

        fireEvent.change(screen.getByPlaceholderText('Add a comment'), { target: { value: 'New Comment' } });
        expect(screen.getByPlaceholderText('Add a comment')).toHaveValue('New Comment');

        fireEvent.click(addButton);

        await waitFor(() => expect(mockAddComment).toHaveBeenCalledWith(testArticleId, 'New Comment'));
        expect(screen.getByText('New Comment')).toBeInTheDocument();
    });

    test('UT-9.4: allows editing and deleting an existing comment', async () => {
        await act(async () => {
            render(<CommentsSidebar articleId={testArticleId} onClose={jest.fn()} />);
        });

        // Ensure the initial comment is displayed
        await waitFor(() => expect(screen.getByText('Initial Comment')).toBeInTheDocument());

        // Edit the comment
        const editButton = screen.getByText('Edit');
        fireEvent.click(editButton);

        const editTextarea = screen.getByDisplayValue('Initial Comment');
        fireEvent.change(editTextarea, { target: { value: 'Edited Comment' } });
        const saveButton = screen.getByText('Save');
        fireEvent.click(saveButton);

        // Confirm the edit
        await waitFor(() => expect(mockEditComment).toHaveBeenCalledWith(initialComment.comment_id, 'Edited Comment'));
        expect(screen.getByText('Edited Comment')).toBeInTheDocument();

        await waitFor(() =>{ const editButton2 = screen.getByText('Edit');
        fireEvent.click(editButton2);
        },{timeout:5000});

        // Delete the comment
        await waitFor(() =>{ const deleteButton = screen.getByText('Delete');
        fireEvent.click(deleteButton);
    },{timeout:5000});
        await waitFor(() => expect(mockDeleteComment).toHaveBeenCalledWith(initialComment.comment_id));
        expect(screen.queryByText('Edited Comment')).not.toBeInTheDocument();
    });
});
