import './App.css';
import Thing from './Frontend/Thing'
import { useReducer } from 'react';
import { positionContext, positionInitial, positionReducer } from './Frontend/ThingHelper/factory'
import { peopleContext, peopleInitial, peopleReducer } from './Frontend/ThingHelper/factory'

function App() {
  const [position, setPosition] = useReducer(positionReducer, positionInitial)
  const [people, setpeople] = useReducer(peopleReducer, peopleInitial)

  return (
    <div className="App">
      <peopleContext.Provider value={{ get: people, set: setpeople }}>
        <positionContext.Provider value={{ get: position, set: setPosition }}>
          <Thing />
        </positionContext.Provider>
      </peopleContext.Provider>
    </div>
  );
}

export default App;
