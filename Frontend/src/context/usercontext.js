// src/contexts/UserContext.js
import { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext(null);

export const UserProvider = ({ children }) => {


    useEffect(() => {
        //aller cherher les données dans le local storage
        const user = localStorage.getItem('da8063c9-acbf-44f0-bf58-85b7728f1d45.c7d1a8f7-0546-4a0c-8cf5-3ddaebf97d51-login.windows.net-c7d1a8f7-0546-4a0c-8cf5-3ddaebf97d51');
        console.log(user);  

    }, []);

    return (
        <UserContext.Provider value={{ }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
