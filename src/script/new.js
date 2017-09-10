import React from 'react';
import ReactDOM from 'react-dom';

class Header extends React.Component{
  constructor(){
    super();
    this.state = {title:'Tank Overflow',p1:'Question',p2:'Blog',p3:'Projects'}
  }
  render() {
    return (
      <header className="mdl-layout__header mdl-layout__header--scroll">
        <div className="mdl-layout__header-row">
            <a href="/"><span className="mdl-layout-title">{this.state.title}</span></a>
            <div className="mdl-layout-spacer"></div>
          <nav className="mdl-navigation">
            <a className="mdl-navigation__link" href="/question">{this.state.p1}</a>
            <a className="mdl-navigation__link" href="/blog">{this.state.p2}</a>
            <a className="mdl-navigation__link" href="/question">{this.state.p3}</a>
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
