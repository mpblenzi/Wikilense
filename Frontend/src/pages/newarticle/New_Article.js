import React, { useEffect, useState } from 'react';
import Header from '../../composant/header/header';
import Footer from '../../composant/footer/footer';
import { useUser } from '../../context/usercontext';

function NewArticle() {
    const [technologies, setTechnologies] = useState([]);
    const [categories, setCategories] = useState([]);
    const [subcategories, setSubcategories] = useState([]);
    const [selectedTechnology, setSelectedTechnology] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSubcategory, setSelectedSubcategory] = useState('');
    const [title, setTitle] = useState('');
    const [file, setFile] = useState(null);
    const { user, setUser } = useUser();

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

        // // À déclencher à nouveau lorsqu'une catégorie est sélectionnée pour charger les sous-catégories correspondantes
        // if (selectedCategory) {
        //     fetch(`http://localhost:5000/category/souscategory/by_id?category=${selectedCategory}`)
        //         .then(response => response.json())
        //         .then(data => setSubcategories(data))
        //         .catch(error => console.error('Error fetching subcategories:', error));
        // }

    }, [selectedTechnology, selectedCategory]);

    const handleSubmit = (event) => {
        event.preventDefault();

        //si tou les champs sont remplis
        if (selectedTechnology && selectedCategory && title && file) {
            // Créer un FormData pour envoyer le fichier
            const formData = new FormData();
            formData.append('file', file); // 'file' est le nom de la clé attendue par votre API
            formData.append('title', title); // Envoyer d'autres données si nécessaire
            // Ajoutez d'autres champs si nécessaire
            // formData.append('technology', selectedTechnology);
            // formData.append('category', selectedCategory);
            // formData.append('subcategory', selectedSubcategory);
        
            // Envoyer le formulaire avec fetch
            fetch('http://localhost:5000/article/upload', {
                method: 'POST',
                body: formData, // Pas besoin de spécifier le content-type header pour multipart/form-data
            })
            .then(response => response.json())
            .then(data => {
                //console.log(data); // Traiter la réponse du serveur
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
        }
        else {
            alert('saisir tous les champs obligatoires');
        }
    };
    
    // Gestionnaire pour le changement de fichier
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    return (
        <div>
            <Header />
            <div style={{ margin: '0 auto', padding: '20px' }}>
                <h2>Create a New Article</h2>

                <div>
                    {user ? <p>Hello, {user}</p> : <p>No user logged in</p>}
                </div>
                <form>
                    <label>
                        Choose a technology:
                        <select
                            value={selectedTechnology}
                            onChange={(e) => {
                                setSelectedTechnology(e.target.value);
                                setSelectedCategory(''); // Réinitialiser les catégories et sous-catégories
                                setSelectedSubcategory(''); // Réinitialiser les sous-catégories
                            }}
                        >
                            <option value="">Choose technology</option>
                            {technologies.map((tech) => (
                                <option key={tech.ID} value={tech.ID}>{tech.Nom}</option>
                            ))}
                        </select>
                    </label>

                    {selectedTechnology && (
                        <label>
                            Choose a category:
                            <select
                                value={selectedCategory}
                                onChange={(e) => {
                                    setSelectedCategory(e.target.value);
                                    setSelectedSubcategory(''); // Réinitialiser les sous-catégories
                                }}
                            >
                                <option value="">Choose category</option>
                                {categories.map((cat) => (
                                    <option key={cat.ID} value={cat.ID}>{cat.Nom}</option>
                                ))}
                            </select>
                        </label>
                    )}
                    {/* 
                    {selectedCategory && (
                        <label>
                            Choose a subcategory (optional):
                            <select 
                                value={selectedSubcategory}
                                onChange={(e) => setSelectedSubcategory(e.target.value)}
                            >
                                <option value="">Choose subcategory</option>
                                {subcategories.map((subcat) => (
                                    <option key={subcat.id} value={subcat.id}>{subcat.name}</option>
                                ))}
                            </select>
                        </label>
                    )} */}

                    <label>
                        Choose a title for your article:
                        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Type your title here..." />
                    </label>
                    <label>
                        Upload your Word file:
                        <input type="file" onChange={handleFileChange} />
                        <span>{file ? file.name : "No file selected"}</span>
                    </label>
                    <div>
                        <button type="button">Cancel</button>
                        <button type="submit" onClick={handleSubmit} >Publish article</button>
                    </div>
                </form>
            </div>
            <Footer />
        </div>
    );
}

export default NewArticle;
