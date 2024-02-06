import React from 'react';
import './acceuil.css';
import { useState,useEffect } from 'react';
import { useMsalAuthentication } from '@azure/msal-react';
import { InteractionType } from '@azure/msal-browser';
import { fetchData } from '../../Fetch';

import Header from '../../composant/header/header';
import Footer from '../../composant/footer/footer';
import CategoryGrid from '../../composant/categoryGrid/categoryGrid';

function Acceuil() {

    const [data, setData] = useState(null);
    const {result, error} = useMsalAuthentication(InteractionType.Popup, {
        scopes: ["User.Read"],
    });
    const [Category, setCategory] = useState([]);

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
        fetch('http://localhost:5000/data/category')
          .then(response => response.json())
          .then(Category => setCategory(Category));
      }, []);

      useEffect(() => {
        if (Category) {
            // Créer un tableau de promesses pour charger toutes les images
            console.log(Category);
            const imagePromises = Category.map((category) => {
                return fetch('http://localhost:5000/images_category/' + category[2]) // Assurez-vous que 'category.id' est la bonne clé pour l'ID de votre catégorie
                    .then(response => response.url);
            });
    
            Promise.all(imagePromises)
                .then(images => {
                    // Mettre à jour chaque catégorie avec son URL d'image dans un nouveau tableau
                    const updatedCategories = Category.map((category, index) => ({
                        ...category,
                        imageUrl: images[index], // Assumer que 'images' est dans le même ordre que 'Category'
                    }));
    
                    setCategory(updatedCategories); // Mettre à jour l'état avec les nouvelles données
                })
                .catch(error => console.log(error));

                console.log(Category);
        }       
    }, [Category]);


    return (
        <div>
            <Header/>
                <p>Hello {data?.displayName}, welcome to Wikilens</p>
                <p>Discover general technical informations about lens and frame manufacturing</p>

                <div>
                    <CategoryGrid categories={Category} />
                </div>

                <button>Add and acticle </button>
            <Footer/>
        </div>
    );
}

export default Acceuil;
