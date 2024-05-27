import React, { useState, useEffect } from 'react';
import './acceuil.css';
import { useNavigate } from 'react-router-dom';
import Header from '../../composant/header/header';
import Footer from '../../composant/footer/footer';
import CategoryGrid from '../../composant/categoryGrid/categoryGrid';
import { useMsal } from '@azure/msal-react';

function Acceuil() {
  const [Category, setCategory] = useState([]);
  const { instance } = useMsal();
  const account = instance.getActiveAccount();

  useEffect(() => {
    fetch('http://localhost:5000/category')
      .then(response => response.json())
      .then(Category => setCategory(Category));
  }, []);

  useEffect(() => {
    if (Category) {
      const imagePromises = Category.map((category) => {
        return fetch('http://localhost:5000/image/images_category/' + category.Path)
          .then(response => response.url);
      });

      Promise.all(imagePromises)
        .then(images => {
          const updatedCategories = Category.map((category, index) => ({
            ...category,
            imageUrl: images[index],
          }));

          if (JSON.stringify(Category) !== JSON.stringify(updatedCategories)) {
            setCategory(updatedCategories);
          }
        })
        .catch(error => console.log(error));
    }
  }, [Category]);

  useEffect(() => {
    fetch('http://localhost:5000/user/by_email/' + account.username)
      .then(response => response.json())
      .then(data => {
        if (data.Status === 404) {
          fetch('http://localhost:5000/user/add_user', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: account.username,
              name: account.name,
              token: account.idToken,
              id: account?.idTokenClaims?.oid
            }),
          })
          .then(response => response.json())
          .then(data => {
            if (data.status === 200) {
              console.log('User created successfully');
            }
          })
          .catch(error => console.error('Error creating user:', error));
        }
      })
      .catch(error => console.error('Error fetching user:', error));
  }, []);

  let navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/NewArticle'); // Remplacez par le chemin de votre choix
  };

  return (
    <div className='Acceuil'>
      <Header/>
      <div className='MessageDeBienvenueAccueil'>
        <h1>Hello {account.name}, welcome to Wikilens</h1>
        <h2>Discover general technical informations about lens and frame manufacturing</h2>
      </div>
      <div>
        <CategoryGrid categories={Category} />
      </div>
      <div className='BoutonAddAnArticleContainer'>
        <button onClick={handleButtonClick} className='BoutonAddAnArticle'>
          <i className="uil uil-plus-circle"></i>Add an article
        </button>
      </div>
      {/* <Footer/> */}
    </div>
  );
}

export default Acceuil;
