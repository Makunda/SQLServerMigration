import React from 'react';
import logo from './resources/images/logo.svg';
import './resources/css/App.css';
import "@react-sigma/core/lib/react-sigma.min.css"
import {WelcomeComponent} from "./components/default/WelcomeComponent";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <WelcomeComponent></WelcomeComponent>
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
