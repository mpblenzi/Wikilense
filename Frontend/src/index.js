import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
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
      storeAuthStateInCookie: false,
  },
  system:{
    loggerOptions:{
      loggerCallback: (level, message, containsPii) => {
      },
    }
  }
});

pca.addEventCallback((event) => {
  if (event.eventType === EventType.LOGIN_SUCCESS) {
      pca.setActiveAccount(event.payload.account);
  }
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App msalInstance={pca} />
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
