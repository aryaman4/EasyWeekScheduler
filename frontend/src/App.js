import React, { Component } from 'react';
import './App.css';
import { BrowserRouter as Router, Route} from 'react-router-dom';
import Home from './components/home';
import About from './components/about';
import News from './components/news'



class App extends Component {
  render() {
    return (
      <Router>
        <div>
          <Route exact path="/" component = {Home} />
          <Route path="/about" component = {About} />
          <Route path="/test" component = {News} />



        </div>
      </Router>
    );
  }
}

export default App;
