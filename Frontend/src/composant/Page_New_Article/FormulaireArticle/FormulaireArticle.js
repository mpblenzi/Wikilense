import React from 'react';
import SelectionTechnologie from '../SelectionTechnologie/SelectionTechnologie';
import SelectionCategorie from '../SelectionCategorie/SelectionCategorie';
import InputTitre from '../InputTitre/InputTitre';
import TelechargementFichier from '../TelechargementFichier/TelechargementFichier';
import './FormulaireArticle.css';
import { useState } from 'react';

const FormulaireArticle = ({
  technologies, categories, selectedTechnology, setSelectedTechnology,
  selectedCategory, setSelectedCategory, title, setTitle, file, setFile, handleSubmit
}) => {
  return (
    <form>
      <SelectionTechnologie technologies={technologies} selectedTechnology={selectedTechnology} onChange={(e) => {
        setSelectedTechnology(e.target.value);
        setSelectedCategory(''); // Réinitialiser les catégories
      }} />
      {selectedTechnology && <SelectionCategorie categories={categories} selectedCategory={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)} />}
      <InputTitre title={title} setTitle={setTitle} />
      <TelechargementFichier file={file} setFile={setFile} />
      <div>
        <button type="button">Annuler</button>
        <button type="submit" onClick={handleSubmit}>publish</button>
      </div>
    </form>
  );
};

export default FormulaireArticle;

