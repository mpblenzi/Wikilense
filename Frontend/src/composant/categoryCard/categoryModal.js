import React from 'react';
import './categoryModal.css'; // Votre fichier de styles CSS pour le modal

const CategoryModal = ({ category, closeModal }) => {
  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>{category.name}</h2>
        {/* Ici, vous pouvez ajouter plus de contenu ou un composant pour le contenu de la catégorie */}
        <button onClick={closeModal}>Close</button>
      </div>
    </div>
  );
};

export default CategoryModal;
