import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { Router, Route, IndexRoute, hashHistory } from 'react-router';
import Home from './container/Home';
import API from './container/API';
import Graphs from './container/Graphs';

ReactDOM.render(
    <Router history={hashHistory}>
        <Route path='/' component={App}>
            <IndexRoute component={Home} />
            <Route path='/api' component={API} />
            <Route path='/graphs/:id' component={Graphs} />
        </Route>
    </Router>

    ,
    document.getElementById('root'));
registerServiceWorker();