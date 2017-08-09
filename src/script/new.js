import React from 'react';
import ReactDOM from 'react-dom';

class Welcome extends React.Component {
  constructor() {
    super();
    this.state = {title :'Tank OverFlow'}
    }
  render() {
    return(
      <div>
        <h1>{this.state.title}</h1>
      </div>
    );
  }
}

ReactDOM.render(
  <Welcome />,
  document.getElementById('root')
);
