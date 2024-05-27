import React from 'react';
import './TelechargementFichier.css';

const TelechargementFichier = ({ file, setFile }) => (
  <div className='file-upload-container'>
    <input id="file-upload" type="file" onChange={(e) => setFile(e.target.files[0])} />
    <label htmlFor="file-upload" className="custom-file-upload">
      <i className="fa fa-cloud-upload"></i> Upload your Word file
    </label>
    <div className="file-preview">
      {file ? file.name : "No file selected"}
    </div>
  </div>
);

export default TelechargementFichier;
