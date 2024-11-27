import React, { useEffect, useState } from 'react';
import apiCalls from '@/app/api/apiCalls';
import Loading from '../Loading';

interface Comment {
    comment_id: number;
    user_id: number;
    comment_text: string;
    username: string;
    created_at: string;
}

interface CommentsSidebarProps {
    articleId: number;
    onClose: () => void;
    isMobile: boolean;
    setIsCommentButtonPressed: (item: boolean) => void;
    isCommentButtonPressed: boolean;
}

const CommentsSidebar: React.FC<CommentsSidebarProps> = ({ articleId, onClose, isMobile, setIsCommentButtonPressed, isCommentButtonPressed }) => {
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
        if (comments.length >= 100) {
            setError('Cannot add more than 100 comments for this article.');
            return;
        }
        try {
            const addedComment = await addComment(articleId, newComment);
            setComments([...comments, addedComment]);
            setNewComment('');
            setError(null); // Clear any previous errors
        } catch (err) {
            setError('Failed to add comment');
        }
    };

    const handleEditClick = (comment: Comment) => {
        setEditingCommentId(comment.comment_id);
        setEditedText(comment.comment_text);
    };

    const handleSaveEdit = async (comment_id: number) => {
        try {
            const updatedComment = await editComment(comment_id, editedText);
            setComments(comments.map(comment => comment.comment_id === comment_id ? updatedComment : comment));
            setEditingCommentId(null);
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
        <>
            {isMobile && !isCommentButtonPressed ?
                <>
                    <button onClick={() => setIsCommentButtonPressed(true)}
                        className="absolute right-0 top-2/4 bg-white text-black rounded p-2 m-0"
                        style={{ transform: 'rotate(270deg)', marginRight: "-25px" }}
                        data-testid="mobile_comments_button">
                        Comments
                    </button>
                </>
                :
                <>
                    <div className="w-full md:w-1/4 bg-gray-300 overflow-y-auto flex-shrink-0 h-screen" data-testid="comments_sidebar">
                        <div className="p-2 text-black">

                            <div className="justify-end w-full flex">
                                <button
                                    onClick={onClose}
                                    className="text-red-500 hover:text-red-700"
                                    data-testid="comments_sidebar_close"
                                >
                                    ✕
                                </button>
                            </div>

                            <h2 className="font-bold text-xl mb-4 w-full">Comments for Article {articleId}</h2>

                            {loading && <Loading />}
                            {error && <p className="text-red-500">{error}</p>}
                            {comments.length > 0 ? (
                                <ul>
                                    {comments.map((comment, index) => {
                                        let readableTime = "";
                                        if (comment !== null) {
                                            const createdAtDate = new Date(comment.created_at);
                                            readableTime = createdAtDate.toLocaleString('en-US', {
                                                year: 'numeric',
                                                month: 'numeric',
                                                day: 'numeric',
                                                hour: '2-digit',
                                                minute: '2-digit',
                                                second: '2-digit',
                                                hour12: false
                                            });
                                        }
                                        return (
                                            <div key={comment?.comment_id || index} className="bg-white rounded m-2 px-2 pt-2">
                                                <li className="mb-4">
                                                    <div >
                                                        <strong>{comment?.username || "Unknown"} </strong>
                                                        <span className="text-slate-500">
                                                            @ {readableTime !== undefined ? readableTime : ""}
                                                        </span>
                                                        :
                                                        &nbsp;
                                                    </div>
                                                    <div className="">
                                                        {editingCommentId === comment.comment_id ? (
                                                            <>
                                                                <form onSubmit={(e) => { e.preventDefault(); handleSaveEdit(comment.comment_id); }}>
                                                                    <input
                                                                        value={editedText}
                                                                        onChange={e => setEditedText(e.target.value)}
                                                                        className="w-full p-2 border border-gray-300 rounded mb-2"
                                                                    />
                                                                    <button type="submit" className="text-green-500">Save</button>
                                                                </form>
                                                                <button onClick={() => handleDeleteComment(comment.comment_id)} className="text-red-500">
                                                                    Delete
                                                                </button>
                                                            </>
                                                        ) : (
                                                            <>
                                                                <div>{comment?.comment_text || "No comment text available"}</div>
                                                                <button onClick={() => handleEditClick(comment)} className="text-blue-500">
                                                                    Edit
                                                                </button>
                                                            </>
                                                        )}
                                                    </div>
                                                </li>
                                            </div>
                                        )
                                    })}
                                </ul>
                            )
                                :
                                !loading && <p>No comments available.</p>}
                            <div className="mt-4">
                                <form onSubmit={(e) => { e.preventDefault(); handleAddComment() }}>
                                    <input
                                        value={newComment}
                                        onChange={e => setNewComment(e.target.value)}
                                        placeholder="Add a comment"
                                        className="h-16 w-full p-2 border border-gray-300 rounded mb-2"
                                    />
                                    <button type="submit"
                                        className={`bg-blue-500 text-white p-2 rounded ${newComment.trim() === '' ?
                                            'opacity-50 cursor-not-allowed' : ''}`} disabled={newComment.trim() === ''}>
                                        Add Comment
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </>}
        </>
    );
};

export default CommentsSidebar;