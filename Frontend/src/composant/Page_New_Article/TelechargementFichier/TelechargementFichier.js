import React from 'react';

const TelechargementFichier = ({ file, setFile }) => (
  <div>
    <label htmlFor="file-upload" className="custom-file-upload">
      Upload your Word file
    </label>
    <input id="file-upload" type="file" onChange={(e) => setFile(e.target.files[0])} />
    <div className="file-preview">
      {file ? file.name : "No file selected"}
    </div>
  </div>
);

export default TelechargementFichier;
