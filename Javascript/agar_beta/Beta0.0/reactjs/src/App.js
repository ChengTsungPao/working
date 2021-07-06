import './App.css';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import Login from './Login/Login'
import Start from './Start/Start'

import { blobContext, blobInitial, blobReducer } from './index';

function App() {
  const [blob, setBlob] = useReducer(blobReducer, blobInitial);

  return (
    <div className="App">
      <blobContext.Provider value={{ get: blob, set: setBlob }}>
          <Router>
            <Route path = "/" exact component = {Login} />
            <Route path = "/Start" component = {Start}/>
          </Router>
      </blobContext.Provider>
    </div>
  );
}

export default App;
