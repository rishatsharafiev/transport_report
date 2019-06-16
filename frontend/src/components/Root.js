import React from "react";
import { Link, Route, Switch } from "react-router-dom";

import Home from "../views/Home";
import About from "../views/About";

const Root = () => (
  <div className="site-wrapper">
    <header className="site-header">
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
      </ul>
    </header>

    <Switch>
      <Route path="/home" component={Home} />
      <Route path="/about" component={About} />
    </Switch>
  </div>
);

export default Root;
