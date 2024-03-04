// src/contexts/UserContext.js
import { createContext, useContext, useState, useEffect } from 'react';
import { useMsal, useIsAuthenticated } from '@azure/msal-react';


const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
    const [userDetails, setUserDetails] = useState({
        id : null,
        name: null,
        email: null,
        isAuthenticated: false,
    });
    const { instance, accounts } = useMsal();
    const isAuthenticated = useIsAuthenticated();

    useEffect(() => {

        if (isAuthenticated) {
            // Récupération des détails de l'utilisateur connecté
            const account = accounts[0];

            // Récupération de l'ID de l'utilisateur connecté
            fetch(`http://localhost:5000/user/by_email/${account.username}`)
            .then(data => {
                setUserDetails({
                    id: data.ID,
                    name: account.name,
                    email: account.username,
                    isAuthenticated: true,
                });
            }) 
        } else {
            // Utilisateur non authentifié ou déconnecté
            setUserDetails({
                name: null,
                email: null,
                isAuthenticated: false,
            });
        }

        console.log(userDetails);

    }, [isAuthenticated, accounts]);

    const logout = () => {
        instance.logoutPopup().catch(e => {
            console.error(e);
        });
    };

    return (
        <UserContext.Provider value={{ userDetails, setUserDetails, logout }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
