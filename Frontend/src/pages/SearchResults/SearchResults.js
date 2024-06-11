import React from 'react';
import { useLocation } from 'react-router-dom';
import './SearchResults.css';
import Headers from '../../composant/header/header';

function SearchResults() {
    const location = useLocation();
    const { searchTerm, results } = location.state || {};

    return (
        <div>
        <Headers/>
        <div className="search-results-container">
            <h1>Search Results</h1>
            <h2>Results for "{searchTerm}"</h2>
            <div className="results-header">Keyword found in article title</div>
            <ul className="results-list">
                {results && results.map((result, index) => (
                    <li key={index} className="result-item">
                        {/* souligner le titre */}
                        <p className="result-title">{result.Titre}</p>
                        <p className="result-category">{result.Nom} / {result.Nom_parent}</p>
                        {/* <p className="result-excerpt">
                            Small extract from the article body, limited to 160 characters, showing the searched keyword in # A FAIRE DEMAIN 
                        </p>  */}
                    </li>
                ))}
            </ul>
            
            <div className="see-more">See more...</div>
        </div>
        </div>
    );
}

export default SearchResults;
