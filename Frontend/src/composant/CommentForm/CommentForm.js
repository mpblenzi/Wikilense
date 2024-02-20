import React, { useState } from 'react';

const CommentForm = ({ articleId, onCommentSubmitted }) => {
    const [comment, setComment] = useState("");
    // Exemple d'ID utilisateur, devrait être obtenu via authentification/session
    const id_utilisateur = 3; // Ajustez selon votre logique d'authentification

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
