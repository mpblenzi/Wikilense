import React, { useEffect, useState } from 'react';
import './categoryModal.css'; // Assurez-vous que le chemin est correct

const CategoryModal = ({ category, closeModal }) => {
  const [sousCategories, setSousCategories] = useState([]);

  useEffect(() => {
    // Assurez-vous que l'URL est correcte et que votre API est accessible
    fetch(`http://localhost:5000/data/sous-category/${category[0]}`) // Remplacé category[0] par category.id
      .then(response => response.json())
      .then(data => setSousCategories(data))
      .catch(error => console.error("Erreur de fetch:", error));
  }, [category]); // Ajout de category dans le tableau de dépendances pour réexécuter useEffect si category change

  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>{category[1]}</h2>
        <ul>
          {sousCategories.length > 0 && sousCategories.map((sousCategory) => (
            <li key={sousCategory[0]}>{sousCategory[1]}</li>
          ))} 
        </ul>
        <button>Subscribe to this category</button>
        <button onClick={closeModal}>Close</button>
      </div>
    </div>
  );
};

export default CategoryModal;
