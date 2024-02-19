// Dans src/pages/articleDetails/ArticleDetails.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const ArticleDetails = () => {
    const { articleId } = useParams(); // Utilisez useParams pour accéder au paramètre d'URL
    const [article, setArticle] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:5000/article/by_id/${articleId}`)
        .then(response => response.json())
        .then(data => { const articleData = data[0] ? data[0] : null; // Assurez-vous qu'il y a un objet à extraire
        setArticle(articleData);
        })
        .catch(error => console.error("Erreur lors de la récupération de l'article:", error));
    }, [articleId]);

    if (!article) {
    return <div>Chargement de l'article...</div>;
    }

    return (
    <div>
        <h1>{article.Titre}</h1>
        <p>{article.Date_Creation}</p>
        <p>{article.Email}</p>

        
        <p>{article.Nombre_Likes}</p>
        <p>{article.Nombre_Vues}</p>
    </div>
    );
};

export default ArticleDetails;
