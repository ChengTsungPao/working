import './App.css';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import Login from './Login/Login'
import Hall from './Hall/Hall'
import Start from './Start/Start'

function App() {
  return (
    <div className="App">
    <Router>
      <Route path = "/" exact component = {Login} />
      <Route path = "/Hall" component = {Hall}/>
      <Route path = "/Start" component = {Start}/>
    </Router>
    </div>
  );
}

export default App;
