import React from 'react';
import './header.css';

const Header = () => {
    return (
        <header>
            <nav>
                <ul>
                    <li><a href="#">How to use WikiLens</a></li>
                    <li><a href="#">Key numbers</a></li>
                    <li><a href='#'>New article</a></li>
                </ul>   
            </nav>
        </header>
    );
};

export default Header;
