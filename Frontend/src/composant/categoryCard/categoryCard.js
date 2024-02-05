import React from 'react';
import './categoryCard.css'; // Assurez-vous de créer ce fichier CSS
import { useEffect } from 'react';

const CategoryCard = ({ title, imageUrl }) => {

  useEffect(() => {
    console.log(imageUrl);
  }, [imageUrl]);

  return (
    <div className="card">
      <img src={imageUrl} alt={title} className="card-image" />
      <div className="card-title">{title}</div>
    </div>
  );
};

export default CategoryCard;
