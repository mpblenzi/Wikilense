import React from 'react';
import CategoryCard from '../categoryCard/categoryCard'; // Importez le composant de carte ci-dessus
import './categoryGrid.css'; // Assurez-vous de créer ce fichier CSS

const CategoryGrid = ({ categories }) => {
  return (
    <div className="grid">
      {categories.map((category, index) => (
        <CategoryCard key={index} category={category}/>
      ))}
    </div>
  );
};

export default CategoryGrid;
