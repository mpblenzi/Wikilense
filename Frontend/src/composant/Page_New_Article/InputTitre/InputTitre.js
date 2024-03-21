import React from 'react';

const InputTitre = ({ title, setTitle }) => (
  <label>
    Choisissez un titre pour votre article :
    <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title ..." />
  </label>
);

export default InputTitre;
