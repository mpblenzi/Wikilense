import React, { useEffect, useState } from 'react';
import Header from '../../composant/header/header';
import Footer from '../../composant/footer/footer';
import { useMsal } from '@azure/msal-react';
import { Bounce, ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import FormulaireArticle from '../../composant/Page_New_Article/FormulaireArticle/FormulaireArticle';
import './NewArticle.css';

function NewArticle() {
    const [technologies, setTechnologies] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedTechnology, setSelectedTechnology] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSubcategory, setSelectedSubcategory] = useState('');
    const [title, setTitle] = useState('');
    const [file, setFile] = useState(null);
    const { instance } = useMsal();
    const account = instance.getActiveAccount();

    useEffect(() => {
        // Fetch technologies
        fetch('http://localhost:5000/category/')
            .then(response => response.json())
            .then(data => setTechnologies(data))
            .catch(error => console.error('Error fetching technologies:', error));

        // À déclencher à nouveau lorsqu'une technologie est sélectionnée pour charger les catégories correspondantes
        if (selectedTechnology) {
            fetch(`http://localhost:5000/category/souscategory/by_id?technology=${selectedTechnology}`)
                .then(response => response.json())
                .then(data => setCategories(data))
                .catch(error => console.error('Error fetching categories:', error));
        }
    }, [selectedTechnology, selectedCategory]);

    const handleSubmit = (event) => {
        event.preventDefault();

        //si tout les champs sont remplis
        if (selectedTechnology && selectedCategory && title && file) {
            // Créer un FormData pour envoyer le fichier
            const formData = new FormData();
            formData.append('file', file); // 'file' est le nom de la clé attendue par votre API
            formData.append('title', title);
            formData.append('technology', selectedTechnology);
            formData.append('category', selectedCategory);
            formData.append('account_id', account?.idTokenClaims?.oid);
        
            // Envoyer le formulaire avec fetch
            fetch('http://localhost:5000/article/upload', {
                method: 'POST',
                body: formData, // Pas besoin de spécifier le content-type header pour multipart/form-data
            })
            .then(response => response.json())
            .then(data => {
                //si la reponse et 200
                if (data.Status === 200) {
                    toast.success('Article uploaded successfully!');

                    fetch('http://localhost:5000/article/create_article2', {
                        method: 'POST',
                        body: formData, // Pas besoin de spécifier le content-type header pour multipart/form-data
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.Status === 200) {
                            toast.success('Article created successfully!');
                        }
                        else {
                            toast.error('An error occurred while uploading the article. Please try again.');
                        }
                    })

                    // Réinitialiser les champs
                    setSelectedTechnology('');
                    setSelectedCategory('');
                    setSelectedSubcategory('');
                    setTitle('');
                    setFile(null);
                }
                else {
                    toast.error('An error occurred while uploading the article. Please try again.', {
                        position: "bottom-center",
                        autoClose: 5000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                    });
                }
            })
        }
        else {
            alert('Please fill in all fields and select a file to upload.');
        }
    };

    return (
        <div>
            <Header />
            <div className='Create_article'>
                <h2>Create a New Article</h2>
                <ToastContainer
                    position="bottom-center"
                    autoClose={5000}
                    hideProgressBar={false}
                    newestOnTop={false}
                    closeOnClick
                    rtl={false}
                    pauseOnFocusLoss={false}
                    draggable
                    pauseOnHover={false}
                    theme="dark"
                    transition={Bounce}
                />

                <div>
                    <FormulaireArticle
                        technologies={technologies}
                        categories={categories}
                        selectedTechnology={selectedTechnology}
                        setSelectedTechnology={setSelectedTechnology}
                        selectedCategory={selectedCategory}
                        setSelectedCategory={setSelectedCategory}
                        selectedSubcategory={selectedSubcategory}
                        setSelectedSubcategory={setSelectedSubcategory}
                        title={title}
                        setTitle={setTitle}
                        file={file}
                        setFile={setFile}
                        handleSubmit={handleSubmit}
                    />
                </div>
            </div>
            {/* <Footer /> */}
        </div>
    );
}

export default NewArticle;
