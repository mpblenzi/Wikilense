import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './ArticleDetails.css';
import CommentForm from '../../composant/CommentForm/CommentForm';
import CommentsList from '../../composant/CommentsList/CommentsList';
import Footer from '../../composant/footer/footer';
import Header from '../../composant/header/header';

const ArticleDetails = () => {
    const { articleId } = useParams(); // Utilisez useParams pour accéder au paramètre d'URL
    const [articleContent, setArticleContent] = useState(''); // Utiliser une chaîne vide pour initialiser

    useEffect(() => {
        // Assurez-vous que l'URL est correcte et pointe vers votre API backend
        fetch(`http://localhost:5000/article/${articleId}`)
        .then(response => response.text()) // Traiter la réponse comme du texte
        .then(data => setArticleContent(data))
        .catch(error => console.error("Erreur lors de la récupération de l'article:", error));
    }, []);

    const handleCommentSubmitted = () => {
        // Recharger le contenu de l'article après la soumission d'un commentaire
        fetch(`http://localhost:5000/article/${articleId}`)
        .then(response => response.text())
        .then(data => setArticleContent(data))
        .catch(error => console.error("Erreur lors de la récupération de l'article:", error));
        
    };
    
    // Pas besoin de vérifier si article est null ici car la valeur initiale est une chaîne vide
    return (
    <div>
        <Header />
        <div className='article-details'>

            <div className="article-button_admin">
                
            </div>

            <div className="article_more_commentaire">
                {/* Utiliser dangerouslySetInnerHTML pour insérer du HTML */}
                <div dangerouslySetInnerHTML={{ __html: articleContent }}></div>

                <CommentForm articleId={articleId} onCommentSubmitted={handleCommentSubmitted} />

                <CommentsList articleId={articleId} />
            </div>
        
        </div>
        <Footer />
    </div>
    );
};

export default ArticleDetails;
