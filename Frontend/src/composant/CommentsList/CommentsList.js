import { useState, useEffect } from "react";
import DeleteCommentButton from "../Delete_commentaire/Delete_commentaire"; // Importer le composant de suppression de commentaire pour l'utiliser dans la liste de commentaires  
import './CommentsList.css';
import { useMsal } from '@azure/msal-react';
import { Bounce, ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import EditCommentButton from "../Edit_commentaire/edit_commentaire";

const CommentsList = ({ articleId }) => {
    const [comments, setComments] = useState([]);
    const { instance } = useMsal();
    const account = instance.getActiveAccount();
    const currentUser = account?.idTokenClaims?.oid;
    const [editCommentId, setEditCommentId] = useState(null);
    const [editContent, setEditContent] = useState('');
    const [deletingComments, setDeletingComments] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:5000/commentaire/Get_comments/${articleId}`)
            .then(response => response.json())
            .then(data => setComments(data))
            .catch(error => console.error("Erreur lors de la récupération des commentaires:", error));
    }, [articleId], [currentUser], [deletingComments], );

    const handleEdit = (comment) => {
        setEditCommentId(comment.ID);
        setEditContent(comment.Contenu);
    };

    const saveEdit = (commentId) => {
        fetch(`http://localhost:5000/commentaire/${commentId}`, {
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

            {comments.map((comment, index) => (
                <div key={index} className={`comment ${deletingComments.includes(comment.ID) ? 'comment-deleting' : ''}`}>
                    <div className="comment-user">{comment.Nom}</div>
                    <span>Posté le {new Date(comment.Date_Publication).toLocaleString()}</span>
                    {editCommentId === comment.ID ? (
                        <textarea
                            value={editContent}
                            onChange={(e) => setEditContent(e.target.value)}
                        />
                    ) : (
                        <p>{comment.Contenu}</p>
                    )}
                    {comment.ID_Utilisateur === currentUser && (
                        <div className="comment-actions">
                            {editCommentId === comment.ID ? (
                                <>
                                    <button onClick={() => saveEdit(comment.ID)}>Sauvegarder</button>
                                    <button onClick={cancelEdit}>Annuler</button>
                                </>
                            ) : (
                                <>
                                    <EditCommentButton comment={comment} onEdit={handleEdit} />
                                    <DeleteCommentButton
                                        commentId={comment.ID}
                                        onCommentDeleting={() => setDeletingComments(current => [...current, comment.ID])}
                                        onCommentDeleted={() => {
                                            setDeletingComments(current => current.filter(id => id !== comment.ID));
                                            handleCommentDeleted(comment.ID);
                                        }}
                                    />
                                </>
                            )}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default CommentsList;