import React from 'react';
import CategoryCard from '../categoryCard/categoryCard'; // Importez le composant de carte ci-dessus
import './categoryGrid.css'; // Assurez-vous de créer ce fichier CSS

const CategoryGrid = ({ categories }) => {
  return (
    <div className="grid">
      {categories.map((category) => (
        <CategoryCard key={category[1]} title={category[1]} imageUrl={category.imageUrl} />
      ))}
    </div>
  );
};

export default CategoryGrid;
