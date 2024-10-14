import React, { useEffect, useState } from 'react';

interface Comment {
    id: number;
    user: string;
    text: string;
    err: string;
}

interface CommentsSidebarProps {
    articleId: number;
}

const CommentsSidebar: React.FC<CommentsSidebarProps> = ({ articleId }) => {
    const [comments, setComments] = useState<Comment[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchComments = async () => {
            try {
                const response = await fetch(`/api/comments?articleId=${articleId}`);
                const data = await response.json();
                setComments(data);
            } catch (err) {
                if (err instanceof Error) {
                    console.error('Error fetching comments:', err.message);
                } else {
                    console.error('Unknown error:', err);
                }
            }
        };
    
        fetchComments();
    }, [articleId]);    

    return (
        <div className="p-4">
            <h2 className="font-bold text-xl mb-4">Comments for Article {articleId}</h2>
            {loading && <p>Loading comments...</p>}
            {error && <p className="text-red-500">{error}</p>}
            {comments.length > 0 ? (
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