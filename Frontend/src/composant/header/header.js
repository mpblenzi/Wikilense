import React from 'react';
import './header.css';

import {Link } from 'react-router-dom';
import SearchBar from '../searchBar/searchBar';
import NotificationIcon from '../notification_icon/notification_icon';

const Header = () => {

    return (
      <div className="class-header">
        {/* Logo sur la gauche avev image dans le dossier assets*/}
        
        <Link to="/">
          <img src="/assets/New wikilens logo (1).png" alt="Logo gauche" className="logo"/>
        </Link>

        {/* Liens et barre de recherche au centre */}
        <div className="center-content">
          
          {/* Liens */}
          <div className="links">
          <Link to="/how_to_use_Wikilense">FAQ</Link> 
          <Link to="/key_numbers">Key figures</Link> 
          <Link to="/new_articles">New articles</Link> 
          </div>

          <div className='reserche-notification'>
            {/* Barre de recherche */}
            <SearchBar/>

            {/* Icône de notification */}
            <NotificationIcon/>
          </div>
        </div>

        <div className="right-content">
          {/* Logo sur la droite */}
          <img src="/assets/LOFT TKS white logo HD (1).png" alt="Logo droite" className="logo-Right" />
          {/*Rajouter le logo essilor luxo */}
          <img src="/assets/EssilorLuxottica white logo.png" alt="Logo droite" className="logo-Right" />
        </div>
        

      </div>
    );
  }
    
  export default Header;
