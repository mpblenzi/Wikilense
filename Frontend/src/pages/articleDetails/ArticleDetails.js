import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './ArticleDetails.css';
import CommentForm from '../../composant/CommentForm/CommentForm';
import CommentsList from '../../composant/CommentsList/CommentsList';
import Header from '../../composant/header/header';

const ArticleDetails = ({ user_id }) => {
    const { articleId } = useParams();
    const [articleContent, setArticleContent] = useState('');
    const [comments, setComments] = useState([]);
    const [reloadComments, setReloadComments] = useState(false);

    useEffect(() => {
        fetch(`http://localhost:5000/article/${articleId}?user_id=${user_id['user_id']}`)
            .then(response => response.text())
            .then(data => setArticleContent(data))
            .catch(error => console.error("Erreur lors de la récupération de l'article:", error));
    }, [articleId, user_id]);

    useEffect(() => {
        fetch(`http://localhost:5000/commentaire/Get_comments/${articleId}`)
            .then(response => response.json())
            .then(data => setComments(data))
            .catch(error => console.error("Erreur lors de la récupération des commentaires:", error));
    }, [articleId, reloadComments]);

    const handleCommentSubmitted = () => {
        setReloadComments(prev => !prev); // Toggle reloadComments to trigger useEffect
    };

    return (
        <div>
            <Header />
            <div className='article-details'>
                <div className="article-button_admin"></div>
                <div className="article_more_commentaire">
                    <div dangerouslySetInnerHTML={{ __html: articleContent }}></div>
                    <CommentForm articleId={articleId} onCommentSubmitted={handleCommentSubmitted} />
                    <CommentsList articleId={articleId} comments={comments} />
                </div>
            </div>
        </div>
    );
};

export default ArticleDetails;
