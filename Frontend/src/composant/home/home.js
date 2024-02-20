import Acceuil from "../../pages/acceuil/acceuil";
import { SignInButton } from "../ButtonSigniIn/SignInButton";
import { useIsAuthenticated } from '@azure/msal-react';

const Home = () => {

    const isAuthenticated = useIsAuthenticated();

    return (
        <div>
            {isAuthenticated ? <Acceuil/> : <SignInButton/>}   
        </div>
    );
};

export default Home;
