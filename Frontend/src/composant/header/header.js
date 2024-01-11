import React from 'react';
import './header.css';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';

// Tes composants
import How_to_use_Wikilense from '../../pages/how_to_use_Wikilense/how_to_use_Wikilense';
import Key_numbers from '../../pages/key_numbers/key_numbers';
import New_articles from '../../pages/new_articles/new_articles';

const Header = () => {
    return (
        <Router>
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

                <Routes>
                    <Route path="/how_to_use_wikiLens" element={<How_to_use_Wikilense />} />
                    <Route path="/key_numbers" element={<Key_numbers />} />
                    <Route path="/new_articles" element={<New_articles />} />
                </Routes>
            </div>
        </Router>
    );
};

export default Header;
