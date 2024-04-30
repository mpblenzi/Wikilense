// CommentItem.js
import React from 'react';
import DeleteCommentButton from "../Delete_commentaire/Delete_commentaire";
import EditCommentButton from "../Edit_commentaire/edit_commentaire";
import ReplyCommentButton from "../Reply_commentaire/reply_commentaire";
import './Commentaire.css';
import LikeButton from '../Like_commentaire/Like_commentaire';

const CommentItem = ({
    comment,
    currentUser,
    onDelete,
    onEditInit,
    onEditSave,
    onEditCancel,
    onReplyInit,
    onReplySend,
    editCommentId,
    setEditContent,
    editContent,
    replyToCommentId,
    replyContent,
    setReplyContent,
    deletingComments
}) => {
    return (
        <div>
            <div className={`comment ${deletingComments?.includes(comment.ID) ? 'comment-deleting' : ''}`}>
                <div className="comment-user">{comment.Nom}</div>
                <span>Posté le {new Date(comment.Date_Publication).toLocaleString()}</span>

                {comment.Modifier && <span> Modifier</span>}

                {editCommentId === comment.ID ? (
                    <textarea
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                    />
                ) : (
                    <p>{comment.Contenu}</p>
                )}

                <div className="Button-action">
                    <ReplyCommentButton comment={comment} onReplyClick={() => onReplyInit(comment.ID)} />
                    {replyToCommentId === comment.ID && (
                        <div>
                            <textarea
                                value={replyContent}
                                onChange={(e) => setReplyContent(e.target.value)}
                            ></textarea>
                            <button onClick={() => onReplySend(comment.ID)}>Envoyer Réponse</button>
                        </div>
                    )}

                    <LikeButton
                        commentId={comment.ID}
                        initialLikesCount={comment.Nombre_Likes || 0}
                        isInitiallyLikedByCurrentUser={comment.CurrentUserHasLiked || false}
                        userId={currentUser}
                        onToggle={(commentId, shouldLike) => {
                            return new Promise((resolve, reject) => {
                                const action = shouldLike ? 'like_comment' : 'unlike_comment';
                                fetch(`http://localhost:5000/like/${action}/${commentId}`, {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify({ID_Utilisateur: currentUser})
                                })
                                .then(response => {
                                    if (!response.ok) {
                                        throw new Error('Could not perform the action');
                                    }
                                    resolve(true);
                                })
                                .catch(error => {
                                    console.error('Error:', error);
                                    reject(error);
                                });
                            });
                        }}
                    />

                    {comment.ID_Utilisateur === currentUser && (
                        <div className="comment-actions">
                            {editCommentId === comment.ID ? (
                                <>
                                    <button onClick={() => onEditSave(comment.ID)}>Sauvegarder</button>
                                    <button onClick={onEditCancel}>Annuler</button>
                                </>
                            ) : (
                                <>
                                    <EditCommentButton comment={comment} onEdit={() => onEditInit(comment)} />
                                    <DeleteCommentButton
                                        commentId={comment.ID}
                                        onCommentDeleting={() => onDelete(comment.ID)}
                                    />
                                </>
                            )}
                        </div>
                    )}
                </div>


            </div>

            {comment.Reponses && comment.Reponses.length > 0 && (
                <div className="replies">
                    {comment.Reponses.map((reply) => (
                        <CommentItem
                            key={reply.ID}
                            comment={reply}
                            currentUser={currentUser}
                            onDelete={onDelete}
                            onEditInit={onEditInit}
                            onEditSave={onEditSave}
                            onEditCancel={onEditCancel}
                            onReplyInit={onReplyInit}
                            onReplySend={onReplySend}
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
            )}
        </div>
    );
};

export default CommentItem;
