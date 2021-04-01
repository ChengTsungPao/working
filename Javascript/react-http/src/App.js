import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react'
import PostList from './components/PostList';
import PostForm from './components/PostForm';

export class App extends Component {
  render() {
    return (
      <div className = "App">
        <PostForm />
        {/* <PostList /> */}
      </div>
    )
  }
}

export default App

