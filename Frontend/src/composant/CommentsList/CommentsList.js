import { useState, useEffect } from "react";
import './CommentsList.css';
import { useMsal } from '@azure/msal-react';
import {ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import CommentItem from "../Commentaire/Commentaire";

const CommentsList = ({ articleId }) => {
    const [comments, setComments] = useState([]);
    const { instance } = useMsal();
    const account = instance.getActiveAccount();
    const currentUser = account?.idTokenClaims?.oid;
    const [editCommentId, setEditCommentId] = useState(null);
    const [editContent, setEditContent] = useState('');
    const [deletingComments, setDeletingComments] = useState([]);
    const [replyToCommentId, setReplyToCommentId] = useState(null);
    const [replyContent, setReplyContent] = useState("");

    function actualiser_com() {
        fetch(`http://localhost:5000/commentaire/Get_comments/${articleId}`)
            .then((response) => {
                if (!response.ok) {
                throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setComments(data);
                console.log(data);
            })
            .catch((error) => {
                console.error('There has been a problem with your fetch operation:', error);
            }
        );
    }


    const handleReplyClick = (commentId) => {
        setReplyToCommentId(commentId);
        // Optionnellement, réinitialiser replyContent ici si vous le souhaitez
        setReplyContent("");
    };

    useEffect(() => {
        actualiser_com();
    }, [articleId], [currentUser], [deletingComments], [editCommentId]);


    const handleEdit = (comment) => {
        setEditCommentId(comment.ID);
        setEditContent(comment.Contenu);
        
    };

    const saveEdit = (commentId) => {
        fetch(`http://localhost:5000/commentaire/edit/${commentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                // Ajoute les headers nécessaires ici, comme les tokens d'authentification si nécessaire
            },
            body: JSON.stringify({ content: editContent }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erreur lors de la mise à jour du commentaire');
                }
                return response.json();
            })
            .then(data => {
                setComments(currentComments => currentComments.map(comment => {
                    if (comment.ID === commentId) {
                        return { ...comment, Contenu: editContent };
                    }
                    actualiser_com();
                    return comment;
                }));
                setEditCommentId(null); // Reset l'ID de l'édition après sauvegarde
            })
            .catch(error => {
                console.error('Erreur lors de la mise à jour du commentaire:', error);
            });
    };

    const cancelEdit = () => {
        setEditCommentId(null);
    };

    const handleCommentDeleted = (deletedCommentId) => {
        // Supprimer le commentaire de l'état après la suppression et l'animation
        setTimeout(() => {
            setComments(comments.filter(comment => comment.ID !== deletedCommentId));
        }, 500); // Correspond à la durée de l'animation CSS

        toast.success('Commentaire supprimé avec succès');
    };

    const sendReply = (commentId) => {
        // Préparez les données pour l'envoi
        const replyData = {
          ID_Article: articleId, // Supposons que `articleId` soit l'ID de l'article courant passé aux props
          ID_Utilisateur: currentUser, // Vous avez déjà `currentUser` dans votre code
          Contenu: replyContent, // Le contenu de la réponse collecté depuis l'état
          ID_Article_Reply: commentId, // L'ID du commentaire auquel on répond
        };

        // Envoyer la requête POST au backend
        fetch('http://localhost:5000/commentaire/Add_comment_reply/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Incluez ici tout autre header nécessaire, comme les tokens d'authentification
            },
            body: JSON.stringify(replyData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Échec de l’envoi de la réponse');
            }
            return response.json();
        })
        .then(data => {
          console.log(data); // Traitez la réponse du serveur si nécessaire
          actualiser_com(); // Actualisez la liste des commentaires pour afficher la nouvelle réponse
        })
        .catch(error => {
            console.error('Erreur lors de l’envoi de la réponse:', error);
        });

        // Réinitialiser l'état après l'envoi
        setReplyToCommentId(null);
        setReplyContent("");
    };

    return (
        <div className="comments-section">
            <ToastContainer
            position="top-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            />
        
        {comments.map((comment) => (
            <CommentItem
                key={comment.ID}
                comment={comment}
                currentUser={currentUser}
                onDelete={handleCommentDeleted}
                onEditInit={handleEdit}
                onEditSave={saveEdit}
                onEditCancel={cancelEdit}
                onReplyInit={handleReplyClick}
                onReplySend={sendReply}
                editCommentId={editCommentId}
                setEditContent={setEditContent}
                editContent={editContent}
                replyToCommentId={replyToCommentId}
                replyContent={replyContent}
                setReplyContent={setReplyContent}
                deletingComments={deletingComments}
            />
            ))}
        </div>
    );
}

export default CommentsList;