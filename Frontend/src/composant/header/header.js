import React from 'react';
import './header.css';

import {Link } from 'react-router-dom';
import { useState,useEffect } from 'react';
import { useMsalAuthentication } from '@azure/msal-react';
import { InteractionType } from '@azure/msal-browser';
import { fetchData } from '../../Fetch';
import SearchBar from '../searchBar/searchBar';
import Notification_icon from '../notification_icon/notification_icon';

const Header = () => {
    const [data, setData] = useState(null);
    const {result, error} = useMsalAuthentication(InteractionType.Popup, {
        scopes: ["user.Read"],
    });

    useEffect(() => {
        if(!!data){
            console.log("ici",data);
            return;
        }

        if(!!error){
            console.log("ici",error);
            return;
        }

        if(result){
            console.log("ici",result);
            const {accessToken} = result;
            fetchData("https://graph.microsoft.com/v1.0/me", accessToken)
                .then(response => setData(response))
                .catch(error => console.log(error));
            
        }
    }, [data, error, result]);

    return (
        <div className='class-header'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/langfr-220px-Wikipedia-logo-v2.svg.png" alt="logo" className="logo"/>
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
            <SearchBar/>
            <Notification_icon/>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/langfr-220px-Wikipedia-logo-v2.svg.png" alt="logo" className="logo"/>
        </div>
    );
};

export default Header;
