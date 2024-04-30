import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './composant/app/App';
import reportWebVitals from './reportWebVitals';
import { PublicClientApplication, EventType } from '@azure/msal-browser';
import { BrowserRouter } from "react-router-dom";

const pca = new PublicClientApplication({
  auth:{
      clientId: '8ba30e7a-d8c5-4fc5-811a-566652271f09',
      authority:'https://login.microsoftonline.com/c7d1a8f7-0546-4a0c-8cf5-3ddaebf97d51',
      redirectUri:'http://localhost:4200',
  },
  cache:{
      cacheLocation:'localStorage',
      storeAuthStateInCookie: true,
  },
  system:{
    loggerOptions:{
      loggerCallback: (level, message, containsPii) => {
      },
    }
  }
});

async function initializeMsal() {
  try {
    await pca.initialize();
    // Après l'initialisation, rechercher l'iframe généré par MSAL
    const msalIframe = document.querySelector("iframe[src^='https://login.microsoftonline.com']");
    if (msalIframe) {
      // Modifier les attributs sandbox de l'iframe pour désactiver allow-scripts et allow-same-origin
      msalIframe.setAttribute('sandbox', 'allow-forms allow-popups allow-same-origin allow-top-navigation');
    }
  } catch (error) {
    console.error('Error initializing MSAL:', error);
  }
}

initializeMsal();

// Ajouter le gestionnaire d'événements pour login success
pca.addEventCallback((event) => {
  if (event.eventType === EventType.logIN_SUCCESS) {
    pca.setActiveAccount(event.payload.account);
  }
});

initializeMsal().then(() => {
  try {
    createRoot(document.getElementById('root')).render(
      <React.StrictMode>
        <BrowserRouter>
          <App msalInstance={pca} />
        </BrowserRouter>
      </React.StrictMode>
    );
  } catch (error) {
    console.error('Error rendering React application:', error);
  }
});

reportWebVitals();
