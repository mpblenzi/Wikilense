// Dans src/components/CommentForm.js
import React, { useState } from 'react';

const CommentForm = ({ articleId, onCommentSubmitted }) => {
    const [comment, setComment] = useState("");

    const handleCommentSubmit = (e) => {
        e.preventDefault(); // Pour éviter le rechargement de la page
        if (!comment.trim()) return;

        // Remplacer par l'URL de votre API
        fetch(`http://localhost:5000/article/comment/${articleId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ comment }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setComment(""); // Réinitialiser le champ après la soumission
            if (onCommentSubmitted) {
                onCommentSubmitted(); // Callback pour éventuellement rafraîchir les commentaires dans le parent
            }
        })
        .catch(error => console.error("Erreur lors de l'ajout du commentaire:", error));
    };

    return (
        <form onSubmit={handleCommentSubmit}>
            <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Ajouter un commentaire..."
            />
            <button type="submit">Envoyer</button>
        </form>
    );
};

export default CommentForm;
