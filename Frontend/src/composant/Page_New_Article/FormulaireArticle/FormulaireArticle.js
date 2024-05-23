import React from 'react';
import SelectionTechnologie from '../SelectionTechnologie/SelectionTechnologie';
import SelectionCategorie from '../SelectionCategorie/SelectionCategorie';
import InputTitre from '../InputTitre/InputTitre';
import TelechargementFichier from '../TelechargementFichier/TelechargementFichier';
import './FormulaireArticle.css';

const FormulaireArticle = ({
  technologies, categories, selectedTechnology, setSelectedTechnology,
  selectedCategory, setSelectedCategory, title, setTitle, file, setFile, handleSubmit
}) => {
  return (
    <form onSubmit={handleSubmit} className="Create_article">

      <div className="form-group">
        <SelectionTechnologie technologies={technologies} selectedTechnology={selectedTechnology} onChange={(e) => {
          setSelectedTechnology(e.target.value);
          setSelectedCategory(''); // Réinitialiser les catégories
        }} />
      </div>

      {selectedTechnology && (
        <div className="form-group">
          <SelectionCategorie categories={categories} selectedCategory={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)} />
        </div>
      )}

      <div className="form-group">
        <InputTitre title={title} setTitle={setTitle} />
      </div>

      <div className="form-group">
        <TelechargementFichier file={file} setFile={setFile} />
      </div>

      <div className="buttons">
        <button type="button" onClick={() => { /* logiques pour annuler */ }}>Cancel</button>
        <button type="submit">Publish article</button>
      </div>
    </form>
  );
};

export default FormulaireArticle;
