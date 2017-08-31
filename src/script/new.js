import React from 'react';
import ReactDOM from 'react-dom';

class Welcome extends React.Component {
  constructor() {
    super();
    this.state = {title :'Tank OverFlow'}
    }
  render() {
    return(
      <div className="mdl-layout__header mdl-layout__header--waterfall">
        <div className="mdl-layout__header-row">
          <h1 className="mdl-layout-title">{this.state.title}</h1>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <Welcome />,
  document.getElementById('root')
);
