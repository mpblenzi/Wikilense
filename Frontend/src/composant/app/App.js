import './App.css';
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { MsalProvider } from '@azure/msal-react';
import Home from '../home/home';
import About from '../about/about';
import HowToUseWikilense from '../../pages/how_to_use_Wikilense/how_to_use_Wikilense';
import KeyNumbers from '../../pages/key_numbers/key_numbers';
import NewArticles from '../../pages/new_articles/new_articles';
import ArticleDetails from '../../pages/articleDetails/ArticleDetails';
import Acceuil from '../../pages/acceuil/acceuil';
import NewArticle from '../../pages/newarticle/New_Article';
import Footer from '../footer/footer';

function App({ msalInstance }) {
  return (
    <MsalProvider instance={msalInstance}>
      <div className="app">
        <div className="content">
          <Pages />
        </div>
        <Footer />
      </div>
    </MsalProvider>
  );
}

const Pages = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/Accueil" element={<Acceuil />} />
      <Route path="/about" element={<About />} />
      <Route path="/how_to_use_Wikilense" element={<HowToUseWikilense />} />
      <Route path="/key_numbers" element={<KeyNumbers />} />
      <Route path="/new_articles" element={<NewArticles />} />
      <Route path="/articles/:articleId" element={<ArticleDetails />} />
      <Route path="/NewArticle" element={<NewArticle />} />
    </Routes>
  );
};

export default App;
