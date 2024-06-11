import React, { useState } from 'react';
import { useMsal } from '@azure/msal-react';
import './CommentForm.css';

const CommentForm = ({ articleId, onCommentSubmitted }) => {
    const [comment, setComment] = useState("");
    const { instance } = useMsal();
    const account = instance.getActiveAccount();
    const id_utilisateur = account?.idTokenClaims?.oid;

    const handleCommentSubmit = (e) => {
        e.preventDefault();
        if (!comment.trim()) return;

        fetch(`http://localhost:5000/commentaire/Add_comment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ID_Article: articleId,
                ID_Utilisateur: id_utilisateur,
                Contenu: comment
            }),
        })
        .then(response => response.json())
        .then(() =>{
            setComment("");
            onCommentSubmitted();
        })
        .catch(error => console.error("Erreur lors de l'ajout du commentaire:", error));
    };

    return (
        <form onSubmit={handleCommentSubmit} className='comment-form'>
            <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Add a comment..."
            />
            <button type="submit">Post Comment</button>
        </form>
    );
};

export default CommentForm;
