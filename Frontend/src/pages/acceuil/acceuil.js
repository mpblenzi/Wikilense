import React from 'react';
import './acceuil.css';
import { useState,useEffect } from 'react';
import { useMsalAuthentication } from '@azure/msal-react';
import { InteractionType } from '@azure/msal-browser';
import { fetchData } from '../../Fetch';

import Header from '../../composant/header/header';
import Footer from '../../composant/footer/footer';

function Acceuil() {

    const [data, setData] = useState(null);
    const {result, error} = useMsalAuthentication(InteractionType.Popup, {
        scopes: ["User.Read"],
    });

    useEffect(() => {
        if(!!data){
            console.log(data);
            return;
        }

        if(!!error){
            console.log(error);
            return;
        }

        if(result){
            const {accessToken} = result;
            fetchData("https://graph.microsoft.com/v1.0/me", accessToken)
                .then(response => setData(response))
                .catch(error => console.log(error));
            
        }
    }, [data, error, result]);

    return (
        <div>
            <Header/>
                <p>Welcome to Wikilense,{data?.displayName}</p>
            <Footer/>
        </div>
    );
}

export default Acceuil;
