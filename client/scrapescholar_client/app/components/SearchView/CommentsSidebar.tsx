import React, { useEffect, useState } from 'react';
import apiCalls from '@/app/api/apiCalls';

interface Comment {
    comment_id: number;
    user_id: number;
    comment_text: string;
}

interface CommentsSidebarProps {
    articleId: number;
    onClose: () => void;
}

const CommentsSidebar: React.FC<CommentsSidebarProps> = ({ articleId, onClose }) => {
    const [comments, setComments] = useState<Comment[]>([]);
    const [newComment, setNewComment] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [editingCommentId, setEditingCommentId] = useState<number | null>(null);
    const [editedText, setEditedText] = useState<string>('');

    const { getCommentsByArticle, addComment, editComment, deleteComment } = apiCalls();

    useEffect(() => {
        const fetchComments = async () => {
            try {
                const fetchedComments = await getCommentsByArticle(articleId);
                setComments(fetchedComments);
                setLoading(false);
            } catch (err) {
                setError('Failed to load comments');
                setLoading(false);
            }
        };
    
        fetchComments();
    }, [articleId]);

    const handleAddComment = async () => {
        try {
            const addedComment = await addComment(articleId, newComment);
            setComments([...comments, addedComment]);
            setNewComment('');
        } catch (err) {
            setError('Failed to add comment');
        }
    };

    const handleEditClick = (comment: Comment) => {
        setEditingCommentId(comment.comment_id);
        setEditedText(comment.comment_text); // Set the current text for editing
    };

    const handleSaveEdit = async (comment_id: number) => {
        try {
            const updatedComment = await editComment(comment_id, editedText);
            setComments(comments.map(comment => comment.comment_id === comment_id ? updatedComment : comment));
            setEditingCommentId(null); // Exit edit mode after saving
        } catch (err) {
            setError('Failed to edit comment');
        }
    };

    const handleDeleteComment = async (comment_id: number) => {
        try {
            await deleteComment(comment_id);
            setComments(comments.filter(comment => comment.comment_id !== comment_id));
        } catch (err) {
            setError('Failed to delete comment');
        }
    };

    return (
        <div className="p-4 text-black">
            <button 
                onClick={onClose} 
                className="absolute top-0 right-12 mt-2 mr-2 text-red-500 hover:text-red-700"
            >
                ✕
            </button>            
            <h2 className="font-bold text-xl mb-4">Comments for Article {articleId}</h2>

            {loading && <p>Loading comments...</p>}
            {error && <p className="text-red-500">{error}</p>}
            {comments.length > 0 ? (
                <ul>
                    {comments.map((comment, index) => (
                        <li key={comment?.comment_id || index} className="mb-4">
                            <div>
                                <strong>User {comment?.user_id || "Unknown"}</strong>: 
                                {editingCommentId === comment.comment_id ? (
                                    // Editable text area for editing comment
                                    <textarea
                                        value={editedText}
                                        onChange={e => setEditedText(e.target.value)}
                                        className="w-full p-2 border border-gray-300 rounded mb-2"
                                    />
                                ) : (
                                    <span>{comment?.comment_text || "No comment text available"}</span>
                                )}
                            </div>
                            <div className="flex space-x-2">
                                {editingCommentId === comment.comment_id ? (
                                    // Save button after editing
                                    <button onClick={() => handleSaveEdit(comment.comment_id)} className="text-green-500">Save</button>
                                ) : (
                                    <button onClick={() => handleEditClick(comment)} className="text-blue-500">Edit</button>
                                )}
                                <button onClick={() => handleDeleteComment(comment.comment_id)} className="text-red-500">Delete</button>
                            </div>
                        </li>
                    ))}
                </ul>
            ) : !loading && <p>No comments available.</p>}
            
            <div className="mt-4">
                <textarea 
                    value={newComment}
                    onChange={e => setNewComment(e.target.value)}
                    placeholder="Add a comment"
                    className="w-full p-2 border border-gray-300 rounded mb-2"
                />
                <button onClick={handleAddComment} className="bg-blue-500 text-white p-2 rounded">Add Comment</button>
            </div>
        </div>
    );
};

export default CommentsSidebar;