import './App.css';
import React, { useEffect } from 'react';
import Home from '../home/home';
import About from '../about/about';
import { Routes, Route } from 'react-router-dom';
import { MsalProvider, useIsAuthenticated, useMsal } from '@azure/msal-react';
import HowToUseWikilense from '../../pages/how_to_use_Wikilense/how_to_use_Wikilense';
import KeyNumbers from '../../pages/key_numbers/key_numbers';
import NewArticles from '../../pages/new_articles/new_articles';

function App({ msalInstance }) {


  return (
    <MsalProvider instance={msalInstance}>
      <div className="App">
        <body>
          <Pages />
        </body>
      </div>
    </MsalProvider>
  );
}

const Pages = () => {

  const { instance } = useMsal();
  const isAuthenticated = useIsAuthenticated();

  useEffect(() => {
    if (!isAuthenticated) {
      instance.ssoSilent({
        scopes: ["User.Read"],
        loginHint: ""
      }).then((response) => {
        instance.setActiveAccount(response.account)
      }).catch(error => {
        //vider le local storage
        localStorage.clear();
        console.log(error);
      });
    }
  });

  return(
    <Routes>
      <Route path="/" element={<Home/>}/>
      <Route path="/about" element={<About/>}/>
      <Route path="/how_to_use_Wikilense" element={<HowToUseWikilense />} />
      <Route path="/key_numbers" element={<KeyNumbers />} />
      <Route path="/new_articles" element={<NewArticles />} />
    </Routes>
  )
}

export default App;