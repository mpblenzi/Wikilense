import React from 'react';
import './acceuil.css';
import { useNavigate } from 'react-router-dom';
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
        fetch('http://localhost:5000/category')
        .then(response => response.json())
        .then(Category => setCategory(Category));
    }, []);

    

    useEffect(() => {
        if (Category) {
            // Créer un tableau de promesses pour charger toutes les images
            const imagePromises = Category.map((category) => {
                return fetch('http://localhost:5000/image/images_category/' + category.Path) // Assurez-vous que 'category.id' est la bonne clé pour l'ID de votre catégorie
                    .then(response => response.url);
            });
    
            Promise.all(imagePromises)
            .then(images => {
                const updatedCategories = Category.map((category, index) => ({
                    ...category,
                    imageUrl: images[index],
                }));

                // Vérifie si une mise à jour est nécessaire pour éviter la boucle infinie
                if (JSON.stringify(Category) !== JSON.stringify(updatedCategories)) {
                    setCategory(updatedCategories);
                }
            })
            .catch(error => console.log(error));
        }       
    }, [Category]);

    let navigate = useNavigate();

    const handleButtonClick = () => {
        navigate('/NewArticle'); // Remplacez par le chemin de votre choix
    };

    return (
        <div>
            <Header/>
                <div className='MessageDeBienvenueAccueil'>
                    <h1>Hello {data?.displayName}, welcome to Wikilens</h1>
                    <h2>Discover general technical informations about lens and frame manufacturing</h2>
                </div>


                <div>
                    <CategoryGrid categories={Category} />
                </div>
                <div className='BoutonAddAnArticleContainer'>
                    <button onClick={handleButtonClick} className='BoutonAddAnArticle'><i class="uil uil-plus-circle"></i>Add an acticle </button>
                </div>
            <Footer/>
        </div>
    );
}

export default Acceuil;
