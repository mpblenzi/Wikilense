import React from 'react';

const TelechargementFichier = ({ file, setFile }) => (
  <label>
    Téléchargez votre fichier Word :
    <input type="file" onChange={(e) => setFile(e.target.files[0])} />
    <span>{file ? file.name : "Aucun fichier sélectionné"}</span>
  </label>
);

export default TelechargementFichier;
