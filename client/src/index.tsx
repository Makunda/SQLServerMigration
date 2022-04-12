import React from 'react';
import ReactDOM from 'react-dom';
import './resources/css/index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import StatusService from "./services/status/StatusService";
import Logger from "./utils/logging/logger";
import {Provider} from "react-redux";
import store from "./store/store";

const logger = Logger.getLogger("Index declaration")

// Serve the Page
ReactDOM.render(
  <React.StrictMode>
      <Provider store={store}>
        <App />
      </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);


// Get Status of 3rd party services
try {
    const statusService = StatusService.getInstance();
    statusService.initialization();
} catch (e) {
    logger.error("Failed to launch service discovery.", e);
}


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
