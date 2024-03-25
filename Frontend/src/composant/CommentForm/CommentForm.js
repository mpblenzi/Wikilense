import React, { useState } from 'react';
import { useMsal } from '@azure/msal-react';
import './CommentForm.css';


const CommentForm = ({ articleId, onCommentSubmitted }) => {
    const [comment, setComment] = useState("");
    // Exemple d'ID utilisateur, devrait être obtenu via authentification/session
    const { instance } = useMsal();
    const account = instance.getActiveAccount();
    const id_utilisateur =  account?.idTokenClaims?.oid; // Ajustez selon votre logique d'authentification

    const handleCommentSubmit = (e) => {
        e.preventDefault(); // Empêche le rechargement de la page
        if (!comment.trim()) return;

        fetch(`http://localhost:5000/commentaire/Add_comment/`, { // Assurez-vous que cette URL correspond à votre route Flask
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ID_Article: articleId,
                ID_Utilisateur: id_utilisateur, // Assurez-vous d'avoir un moyen d'obtenir cet ID
                Contenu: comment
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setComment("");
            if (onCommentSubmitted) {
                onCommentSubmitted();
            }
        })
        .catch(error => console.error("Erreur lors de l'ajout du commentaire:", error));
    };

    return (
        <form onSubmit={handleCommentSubmit} className='comment-form'>
            <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="add a comment..."
            />
            <button type="submit">Post Comment</button>
        </form>
    );
};

export default CommentForm;
