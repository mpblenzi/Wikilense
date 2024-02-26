import {useState, useEffect } from "react";
import React from 'react';

const CommentsList = ({articleId}) => {

    const [comments, setComments] = useState([]);
    
    useEffect(() => {
        fetch(`http://localhost:5000/commentaire/Get_comments/${articleId}`)
        .then(response => response.json())
        .then(data => setComments(data))
        .catch(error => console.error("Erreur lors de la récupération des commentaires:", error));
    }
    , [articleId]);

    return (
        <div className="comments-section">
            {comments.map((comment, index) => (
                <div key={index} className="comment">
                    <div className="comment-user">{comment.Nom}</div>
                    <p>{comment.Contenu}</p>
                    <span>Posté le {new Date(comment.Date_Publication).toLocaleString()}</span>
                </div>
            ))}
        </div>
    );
};

export default CommentsList;
