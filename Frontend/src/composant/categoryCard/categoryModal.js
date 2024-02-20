import React, { useEffect, useState } from 'react';
import './categoryModal.css';
import { Link } from 'react-router-dom';

const CategoryModal = ({ category, closeModal }) => {
  const [sousCategories, setSousCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:5000/category/sous_categorie_de_categorie/${category.ID}`)
      .then(response => response.json())
      .then(data => {
        // Après avoir récupéré les sous-catégories, initiez les requêtes pour les articles de chaque sous-catégorie
        const promises = data.map(sousCategory =>
          fetch(`http://localhost:5000/article/by_categorie/${sousCategory.ID}`)
            .then(response => response.json())
            .then(articles => ({
              ...sousCategory,
              articles, // Ajoutez les articles récupérés à l'objet de la sous-catégorie
            }))
        );
        Promise.all(promises).then(sousCategoriesWithArticles => {
          setSousCategories(sousCategoriesWithArticles);
          setLoading(false);
        });
      })
      .catch(error => {
        console.error("Erreur de fetch:", error);
        setLoading(false);
      });
  }, [category]);

  if (loading) {
    return <div>Loading...</div>;
  }

 return (
    <div className="modal-overlay" onClick={closeModal}>
      <button>Subscribe to this category</button>
      <button onClick={closeModal}>Close</button>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>{category.nom}</h2>
        <ul>
          {sousCategories.map((sousCategory) => (
            <li key={sousCategory.ID}>
              {sousCategory.Nom}
              <ul>
                {sousCategory.articles.map((article) => (
                  // Utilisez Link pour créer un lien cliquable qui redirige vers la page de l'article
                  <li key={article.id}>
                    <Link to={`/articles/${article.ID}`}>{article.Titre}</Link>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default CategoryModal;
