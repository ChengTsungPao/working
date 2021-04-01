import logo from './logo.svg';
import './App.css';
import React, {useReducer} from 'react'
import ClassCounter from './components/ClassCounter';
import HookCounter from './components/HookCounter';
import HookCounterTwo from './components/HookCounterTwo';
import HookCounterThree from './components/HookCounterThree';
import HookCounterFour from './components/HookCounterFour';
import ClassCounterOne from './components/ClassCounterOne';
import HookCounterOne from './components/HookCounterOne';
import ClassMouse from './components/ClassMouse';
import HookMouse from './components/HookMouse';
import MouseContainer from './components/MouseContainer';
import IntervalClassCounter from './components/IntervalClassCounter';
import IntervalHookCounter from './components/IntervalHookCounter';
import DataFetching from './components/DataFetching';
import ComponentC from './components/ComponentC';
import CounterOne from './components/CounterOne';
import CounterTwo from './components/CounterTwo';
import CounterThree from './components/CounterThree';
import ContextReducerComponentA from './components/ContextReducerComponentA';
import ContextReducerComponentB from './components/ContextReducerComponentB';
import ContextReducerComponentC from './components/ContextReducerComponentC';
import DataFetchingOne from './components/DataFetchingOne';
import DataFetchingTwo from './components/DataFetchingTwo';
import ParentComponent from './components/ParentComponent';
import Counter from './components/Counter';
import FocusInput from './components/FocusInput';
import ClassTimer from './components/ClassTimer';
import HookTimer from './components/HookTimer';
import DocTitleOne from './components/DocTitleOne';
import DocTitleTwo from './components/DocTitleTwo';
import CounterOneCustomHook from './components/CounterOneCustomHook';
import CounterTwoCustomHook from './components/CounterTwoCustomHook';
import UserForm from './components/UserForm';

export const UserContext = React.createContext()
export const ChannelContext = React.createContext()

export const CountContext = React.createContext()
const initialState = 0
const reducer = (state, action) => {
    switch(action){
        case 'increment':
            return state + 1
        case 'decrement':
            return state - 1
        case 'reset':
            return initialState
        default:
            return state
    }
}

// function App() {
//   const [count, dispatch] = useReducer(reducer, initialState)
//   return (
//     <CountContext.Provider value = {{countState: count, countDispatch: dispatch}}>
//       <div className="App">
//         Count - {count}
//         <ContextReducerComponentA />
//         <ContextReducerComponentB />
//         <ContextReducerComponentC />
//       </div>
//     </CountContext.Provider>
//   )
// }

// export default App;


function App() {
  
  return (
    <div className="App">
      <UserForm />
      {/* <CounterTwoCustomHook />
      <CounterOneCustomHook /> */}
      {/* <DocTitleTwo />
      <DocTitleOne /> */}
      {/* <HookTimer />
      <ClassTimer /> */}
      {/* <FocusInput /> */}
      {/* <Counter /> */}
      {/* <ParentComponent /> */}
      {/* <DataFetchingTwo /> */}
      {/* <DataFetchingOne /> */}
      {/* <CounterThree /> */}
      {/* <CounterTwo /> */}
      {/* <CounterOne /> */}
      {/* <UserContext.Provider value = {"Vishwas"}>
        <ChannelContext.Provider value = {"Codevolution"}>
          <ComponentC />
        </ChannelContext.Provider>
      </UserContext.Provider> */}
      {/* <DataFetching /> */}
      {/* <IntervalHookCounter /> */}
      {/* <IntervalClassCounter /> */}
      {/* <MouseContainer /> */}
      {/* <HookMouse /> */}
      {/* <ClassMouse /> */}
      {/* <HookCounterOne /> */}
      {/* <ClassCounterOne /> */}
      {/* <HookCounterFour /> */}
      {/* <HookCounterThree /> */}
      {/* <HookCounterTwo /> */}
      {/* <HookCounter /> */}
      {/* <ClassCounter></ClassCounter> */}
    </div>
  );
}

export default App;
