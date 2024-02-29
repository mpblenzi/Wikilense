import React, { useState } from 'react';
import CategoryModal from './categoryModal'; // Assurez-vous de créer ce composant
import './categoryCard.css'; // Votre fichier de styles CSS

const CategoryCard = ({ category }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <div className="card" onClick={openModal}>
        <img src={category.imageUrl} alt={category.path} className="card-image" />
        <div className="card-title-container">
          <div className="card-title">{category.Nom}</div>
        </div>
      </div>
      {isModalOpen && <CategoryModal category={category} closeModal={closeModal} />}
    </>
  );
};

export default CategoryCard;
