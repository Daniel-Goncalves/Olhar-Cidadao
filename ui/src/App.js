import React, { Component } from 'react';
import './index.css';
import NavBar from './ui/NavBar';
import FinalPage from './container/FinalPage';
class App extends Component {

  render() {
    return (
      <div>
        <NavBar {...this.props}  />
        {this.props.children}
        <FinalPage {...this.props} />
      </div>
        );
      }
    }
    
    export default App;
