import React, { useEffect, useState } from 'react';
import './categoryModal.css';
import { Link } from 'react-router-dom';

const CategoryModal = ({ category, closeModal }) => {
  const [sousCategories, setSousCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    fetch(`http://localhost:5000/category/sous_categorie_de_categorie/${category.ID}`)
      .then(response => response.json())
      .then(data => {
        const promises = data.map(sousCategory =>
          fetch(`http://localhost:5000/article/by_categorie/${sousCategory.ID}`)
            .then(response => response.json())
            .then(articles => ({
              ...sousCategory,
              articles,
            }))
        );
        Promise.all(promises).then(sousCategoriesWithArticles => {
          setSousCategories(sousCategoriesWithArticles);
          setLoading(false);
          setVisible(true);
        });
      })
      .catch(error => {
        console.error("Erreur de fetch:", error);
        setLoading(false);
      });
  }, [category]);

  const closeModalAndReset = () => {
    setVisible(false);
    setTimeout(closeModal, 300);
  };

  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="loading-container">
          <div className="loading-circle"></div>
          <div className="loading-text">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`modal-overlay ${visible ? 'visible' : ''}`} onClick={closeModalAndReset}>
      <div className={`modal-content ${visible ? 'visible' : ''}`} onClick={(e) => e.stopPropagation()}>
        <h2>{category.Nom}</h2>
        {sousCategories.map((sousCategory) => (
          <div key={sousCategory.ID} className="sous-category">
            <div className="sous-category-name">{sousCategory.Nom}</div>
            <div className="articles">
              {sousCategory.articles.map((article) => (
                <div key={article.id} className="article">
                  <Link to={`/articles/${article.ID}`}>{article.Titre}</Link>
                </div>
              ))}
            </div>
          </div>
        ))}
        <div className="modal-divider">
          <button className='SubscribeToThisCategory'>Subscribe to this category <i className="uil uil-bell"></i></button>
          <button className='CloseButtonModalDivider' onClick={closeModalAndReset}>Close <i class="uil uil-times-circle"></i></button>
        </div>
      </div>
    </div>
  );
};

export default CategoryModal;
