import React, { useState } from 'react';

// Fonction de débogage simple
function debounce(func, wait) {
  let timeout;

  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };

    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  // Gérer la mise à jour de la recherche
  const handleSearch = debounce((q) => {
    onSearch(q);
  }, 500); // Attendre 500ms après le dernier événement clé pour lancer la recherche

  return (
    <div role="search">
      <input
        type="text"
        placeholder="Rechercher..."
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          handleSearch(e.target.value);
        }}
        aria-label="Rechercher"
      />
    </div>
  );
};

export default SearchBar;
