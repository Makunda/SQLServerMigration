import React from 'react';
import logo from './resources/images/logo.svg';
import './resources/css/App.css';
import "@react-sigma/core/lib/react-sigma.min.css"
import {WelcomeComponent} from "./components/default/WelcomeComponent";
import MainView from "./components/default/MainView";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <MainView></MainView>

      </header>
    </div>
  );
}

export default App;
