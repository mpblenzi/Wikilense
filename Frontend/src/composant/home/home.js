import { useEffect } from "react";
import Acceuil from "../../pages/acceuil/acceuil";
import { SignInButton } from "../ButtonSigniIn/SignInButton";
import { useIsAuthenticated } from '@azure/msal-react';

const Home = () => {

    const isAuthenticated = useIsAuthenticated();

    useEffect(() => {
        if (isAuthenticated) {
            console.log("User is authenticated");
        } else {
            console.log("User is not authenticated");
        }
    }, [isAuthenticated]);

    return (
        <div>
            {isAuthenticated ? <Acceuil/> : <SignInButton/>}   
        </div>
    );
};

export default Home;
