import React from 'react';
import './header.css';
import {Link } from 'react-router-dom';

const Header = () => {

    return (
        <div>
            <nav>
                <div>
                    <Link to="/how_to_use_Wikilense">How to use WikiLens</Link>
                </div>
                <div>   
                    <Link to="/key_numbers">Key numbers</Link>
                </div>
                <div>   
                <Link to="/new_articles">New articles</Link>
                </div>          
            </nav>
        </div>
    );
};

export default Header;
