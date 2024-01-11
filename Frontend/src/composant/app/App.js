import './App.css';
import React from 'react';
import Header from '../header/header';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <body>
        <Header/>
      </body>
    </div>
  );
}

export default App;
