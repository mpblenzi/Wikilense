import React from 'react';

const SelectionCategorie = ({ categories, selectedCategory, onChange }) => (
  <label>
    Choisissez une catégorie :
    <select value={selectedCategory} onChange={onChange}>
      <option value="">Choisir une catégorie</option>
      {categories.map((cat) => (
        <option key={cat.ID} value={cat.ID}>{cat.Nom}</option>
      ))}
    </select>
  </label>
);

export default SelectionCategorie;
