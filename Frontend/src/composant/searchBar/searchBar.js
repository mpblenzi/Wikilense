import React, { useState } from 'react';

function SearchBar() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  return (
    <input
      type="text"
      placeholder="Recherche..."
      value={searchTerm}
      onChange={handleSearchChange}
    />
  );
}

export default SearchBar;
 