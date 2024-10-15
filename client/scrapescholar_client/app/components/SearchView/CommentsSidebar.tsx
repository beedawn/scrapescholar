import React, { useEffect, useState } from 'react';
import apiCalls from '@/app/api/apiCalls';

interface Comment {
    id: number;
    user: string;
    text: string;
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
                        <li key={comment.id}>
                            <strong>{comment.user}</strong>: {comment.text}
                        </li>
                    ))}
                </ul>
            ) : !loading && <p>No comments available.</p>}
        </div>
    );
};

export default CommentsSidebar;