import { useState, useEffect } from "react";
import './CommentsList.css';
import { useMsal } from '@azure/msal-react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import CommentItem from "../Commentaire/Commentaire";

const CommentsList = ({ articleId, comments: initialComments }) => {
    const [comments, setComments] = useState(initialComments);
    const { instance } = useMsal();
    const account = instance.getActiveAccount();
    const currentUser = account?.idTokenClaims?.oid;
    const [editCommentId, setEditCommentId] = useState(null);
    const [editContent, setEditContent] = useState('');
    const [deletingComments, setDeletingComments] = useState([]);
    const [replyToCommentId, setReplyToCommentId] = useState(null);
    const [replyContent, setReplyContent] = useState("");

    useEffect(() => {
        setComments(initialComments);
    }, [initialComments]);

    const handleReplyClick = (commentId) => {
        setReplyToCommentId(commentId);
        setReplyContent("");
    };

    const handleEdit = (comment) => {
        setEditCommentId(comment.ID);
        setEditContent(comment.Contenu);
    };

    const saveEdit = (commentId) => {
        fetch(`http://localhost:5000/commentaire/edit/${commentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
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
            setEditCommentId(null);
        })
        .catch(error => {
            console.error('Erreur lors de la mise à jour du commentaire:', error);
        });
    };

    const cancelEdit = () => {
        setEditCommentId(null);
    };

    const handleCommentDeleted = (deletedCommentId) => {
        setTimeout(() => {
            setComments(comments.filter(comment => comment.ID !== deletedCommentId));
        }, 500);

        toast.success('Commentaire supprimé avec succès');
    };

    const sendReply = (commentId) => {
        const replyData = {
            ID_Article: articleId,
            ID_Utilisateur: currentUser,
            Contenu: replyContent,
            ID_Article_Reply: commentId,
        };

        fetch('http://localhost:5000/commentaire/Add_comment_reply/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
            setComments([...comments, data]);
            setReplyToCommentId(null);
            setReplyContent("");
        })
        .catch(error => {
            console.error('Erreur lors de l’envoi de la réponse:', error);
        });
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
};

export default CommentsList;
