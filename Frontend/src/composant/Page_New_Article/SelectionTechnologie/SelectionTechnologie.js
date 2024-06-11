import React from 'react';

const SelectionTechnologie = ({ technologies, selectedTechnology, onChange }) => (
  <label>
    Choisissez une technologie :
    <select value={selectedTechnology} onChange={onChange}>
      <option value="">Choisir une technologie</option>
      {technologies.map((tech) => (
        <option key={tech.ID} value={tech.ID}>{tech.Nom}</option>
      ))}
    </select>
  </label>
);

export default SelectionTechnologie;
