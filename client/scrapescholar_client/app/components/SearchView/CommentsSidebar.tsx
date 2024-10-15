import React, { useEffect, useState } from 'react';
import apiCalls from '@/app/api/apiCalls'; // Adjust the path as per your project structure

interface Comment {
    comment_id: number;
    user_id: number;
    comment_text: string;
    article_id: number;
    created_at: string;
}

interface CommentsSidebarProps {
    articleId: number;
}

const CommentsSidebar: React.FC<CommentsSidebarProps> = ({ articleId }) => {
    const [comments, setComments] = useState<Comment[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const { getCommentsByArticle } = apiCalls();

    useEffect(() => {
        const fetchComments = async () => {
            setLoading(true); // Start loading
            try {
                const fetchedComments = await getCommentsByArticle(articleId);
                console.log('Fetched comments:', fetchedComments); // Log comments to debug
                setComments(fetchedComments);
                setError(null);
            } catch (err) {
                setError('Error fetching comments');
            } finally {
                setLoading(false); // Stop loading after fetching
            }
        };

        fetchComments();
    }, [articleId]);

    return (
        <div className="p-4">
            <h2 className="font-bold text-xl mb-4">Comments for Article {articleId}</h2>
            {loading && <p>Loading comments...</p>}
            {error && <p className="text-red-500">{error}</p>}
            {!loading && comments.length > 0 ? (
                <ul>
                    {comments.map((comment) => (
                        <li key={comment.comment_id}>
                            <strong>User {comment.user_id}</strong>: {comment.comment_text || '(No content)'}
                        </li>
                    ))}
                </ul>
            ) : !loading && <p>No comments available.</p>}
        </div>
    );
};

export default CommentsSidebar;