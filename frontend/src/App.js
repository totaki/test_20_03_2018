import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import Main from "./Main";
import Admin from "./Admin";


class App extends Component {
    render() {
        return (
            <Router>
                <div className="App">
                    <div className="container">
                        <h1>Test app</h1>
                        <ul className="nav">
                            <li className="nav-item">
                                <Link to="/" className="nav-link">
                                    Main
                                </Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/admin" className="nav-link">
                                    Admin
                                </Link>
                            </li>
                        </ul>
                        <Route exact path="/" component={Main}/>
                        <Route path="/admin" component={Admin}/>
                    </div>
                </div>
            </Router>
        );
    }
}

export default App;
