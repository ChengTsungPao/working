import logo from './logo.svg';
import './App.css';
import { Greet } from './components/Greet'
import Welcome from './components/Welcome'
import Hello from './components/Hello'
import { Component, PureComponent } from 'react';
import Message from './components/Message'
import Counter from './components/Counter'
import FunctionClick from './components/FunctionClick';
import ClassClick from './components/ClassClick';
import EventBind from './components/EventBind';
import ParentComponent from './components/ParentComponent';
import UserGreeting from './components/UserGreeting';
import NameList from './components/NameList';
import StyleSheet from './components/StyleSheet';
import Inline from './components/Inline';
import './appStyles.css'
import styles from './appStyles.module.css'
import From from './components/Form';
import LifeCycleA from './components/LifeCycleA';
import FragmentDemo from './components/FragmentDemo';
import Table from './components/Table';
import PureComp from './components/PureComp';
import ParentComp from './components/ParentComp';
import RefsDemo from './components/RefsDemo';
import FocusInput from './components/FocusInput';
import FRParentInput from './components/FRParentInput';
import PortalDemo from './components/PortalDemo';
import Hero from './components/Hero';
import ErrorBoundary from './components/ErrorBoundary';
import ClickCounter from './components/ClickCounter';
import HoverCounter from './components/HoverCounter';
import ClickCounterTwo from './components/ClickCounterTwo';
import HoverCounterTwo from './components/HoverCounterTwo';
import User from './components/User';
import CounterTwo from './components/CounterTwo';
import ComponentC from './components/ComponentC';
import { UserConsumer, UserProvider } from './components/userContext';

class App extends Component {
  render() {
    return (
      <div className="App">
        {/* <UserProvider value = "Vishwas">
          <ComponentC />
        </UserProvider> */}
        {/* <CounterTwo render = {(count, incrementCount) => 
          <ClickCounterTwo 
            count = {count} 
            incrementCount = {incrementCount}>
          </ClickCounterTwo>}/>
        <CounterTwo render = {(count, incrementCount) => 
          <HoverCounterTwo 
            count = {count} 
            incrementCount = {incrementCount}>
          </HoverCounterTwo>}/> */}
        {/* <ClickCounterTwo />
        <HoverCounterTwo />
        <User render = {(isLoggedIn) => isLoggedIn ? "Vishwas" : "Guest"}/> */}
        {/* <ClickCounter name = "Vishwas"/>
        <HoverCounter /> */}
        {/* <ErrorBoundary>
          <Hero heroName = "Batman"></Hero>
        </ErrorBoundary>
        <ErrorBoundary>
          <Hero heroName = "Superman"></Hero>
        </ErrorBoundary>
        <ErrorBoundary>
          <Hero heroName = "Joker"></Hero>
        </ErrorBoundary> */}
        {/* <PortalDemo /> */}
        {/* <FRParentInput /> */}
        {/* <FocusInput /> */}
        {/* <RefsDemo /> */}
        {/* <ParentComp /> */}
        {/* <PureComp /> */}
        {/* <Table /> */}
        {/* <FragmentDemo /> */}
        {/* <LifeCycleA /> */}
        {/* <From /> */}
        {/* <h1 className = "error">Error</h1>
        <h1 className = {styles.success}>Success</h1>
        <Inline />
        <StyleSheet primary = {true}/> */}
        {/* <NameList /> */}
        {/* <UserGreeting /> */}
        {/* <ParentComponent /> */}
        {/* <EventBind /> */}
        {/* <FunctionClick />
        <ClassClick /> */}
        {/* <Counter /> */}
        {/* <Message /> */}
        {/* <Greet name = "Bruce" hn = "a">
          <p>This is children props</p>
        </Greet>
        <Greet name = "Clark" hn = "b" >
          <button>Action</button>
        </Greet> */}
        {/* <Greet name = "Diana" hn = "c" />
        <Welcome name = "Bruce" hn = "a" /> */}
        {/* <Welcome name = "Clark" hn = "b" />
        <Welcome name = "Clark" hn = "b" /> */}
        {/* <Hello /> */}
      </div>
    );
  }
}

export default App;
