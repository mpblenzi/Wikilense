// Dans src/pages/articleDetails/ArticleDetails.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './ArticleDetails.css';
import CommentForm from '../../composant/CommentForm/CommentForm';

const ArticleDetails = () => {
    const { articleId } = useParams(); // Utilisez useParams pour accéder au paramètre d'URL
    const [article, setArticle] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:5000/article/article/${articleId}`)
        .then(response => response.json())
        .then(data => setArticle(data))
        .catch(error => console.error("Erreur lors de l'incrémentation des vues:", error));
    }, [articleId]);;

    const handleCommentSubmitted = () => {
        // Vous pourriez vouloir rafraîchir les commentaires ici
    };

    if (!article) {
    return <div>Chargement de l'article...</div>;
    }

    return (
    <div>
        <h1>{article.Titre}</h1>
        <p>{article.Date_Creation}</p>
        <p>{article.Mail}</p>

        <div>
            {article.Contenus.map((contenu, index) => {
                return contenu.type === 'texte' ? (
                    <p key={index}>{contenu.contenu}</p>
                ) : (
                    <img key={index} src={`http://localhost:5000/image/image_article/${contenu.src}`} alt={`Contenu ${index}`} style={{ maxWidth: "100%" }} />
                );
            })}
        </div>
        

        <p>{article.Nombre_Likes}</p>
        <p>{article.Nombre_Vues}</p>

        <CommentForm articleId={articleId} onCommentSubmitted={handleCommentSubmitted} />
    </div>
    );
};

export default ArticleDetails;
