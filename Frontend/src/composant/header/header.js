import React from 'react';
import './header.css';

import {Link } from 'react-router-dom';
import { useState,useEffect } from 'react';
import { useMsalAuthentication } from '@azure/msal-react';
import { InteractionType } from '@azure/msal-browser';
import { fetchData } from '../../Fetch';
import SearchBar from '../searchBar/searchBar';
import NotificationIcon from '../notification_icon/notification_icon';

const Header = () => {
    const [data, setData] = useState(null);
    const {result, error} = useMsalAuthentication(InteractionType.Popup, {
        scopes: ["user.Read"],
    });
    const [user, setUser] = useState(null);

    useEffect(() => {
        if(!!data){
            return;
        }

        if(!!error){
            return;
        }

        if(result){
            //console.log("ici",result);

            //mettre dans user le result.account.username
            setUser(result.account.username);

            const {accessToken} = result;
            fetchData("https://graph.microsoft.com/v1.0/me", accessToken)
                .then(response => setData(response))
                .catch(error => console.log(error));
        }
    }, [data, error, result]);

    return (
        <div className="class-header">
          {/* Logo sur la gauche */}
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/langfr-220px-Wikipedia-logo-v2.svg.png" alt="Logo gauche" className="logo" />
    
          {/* Liens et barre de recherche au centre */}
          <div className="center-content">
            {/* Liens */}
            <div className="links">
              <a href="#">FAQ</a>
              <a href="#">Key figures</a>
              <a href="#">New articles</a>
            </div>
            {/* Barre de recherche */}
            <SearchBar/>            {/* Icône de notification */}
            <i className="uil uil-bell"></i>
          </div>
    
          {/* Logo sur la droite */}
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/langfr-220px-Wikipedia-logo-v2.svg.png" alt="Logo droite" className="logo" />
        </div>
      );
    }
    
    export default Header;
