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

    const [datatest, setDatatest] = useState('');

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

    useEffect(() => {
        fetch('http://localhost:5000/data')
          .then(response => response.json())
          .then(datatest => setDatatest(datatest.message));
      }, []);



    return (
        <div>
            <Header/>
                <p>Hello {data?.displayName}, welcome to Wikilens</p>
                <p>Discover general technical informations about lens and frame manufacturing</p>

                <div>
                    {datatest ? <p>{datatest}</p> : <p>Loading...</p>}
                </div>

                <button>Add and acticle </button>
            <Footer/>
        </div>

    );
}


export default Acceuil;
