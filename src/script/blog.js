import React from 'react';
import ReactDOM from 'react-dom';

class Newpost extends React.Component {
  constructor(){
    super();
    this.state = {}
  }

  render(){
    return (
      <h1>Hello!</h1>
    );
  }
}

ReactDOM.render(
  <Newpost />,
  document.getElementById('npost')
)
