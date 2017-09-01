import React from 'react';
import ReactDOM from 'react-dom';

class Header extends React.Component{
  constructor(){
    super();
    this.state = {title:'Tank Overflow',p1:'Question',p2:'Blog',p3:'Tags',p4:'Projects'}
  }
  render() {
    return (
      <header className="mdl-layout__header mdl-layout__header--scroll">
        <div className="mdl-layout__header-row">
            <span className="mdl-layout-title">{this.state.title}</span>
            <div className="mdl-layout-spacer"></div>
          <nav className="mdl-navigation">
            <a className="mdl-navigation__link" href="">{this.state.p1}</a>
            <a className="mdl-navigation__link" href="">{this.state.p2}</a>
            <a className="mdl-navigation__link" href="">{this.state.p3}</a>
            <a className="mdl-navigation__link" href="">{this.state.p4}</a>
          </nav>
        </div>
      </header>
    );
  }
}

class Welcome extends React.Component {
  render() {
    return(
        <Header />
      );
  }
}

ReactDOM.render(
  <Welcome />,
  document.getElementById('header')
);
