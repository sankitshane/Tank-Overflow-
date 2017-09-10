import React from 'react';
import ReactDOM from 'react-dom';

class InfoTab extends React.Component {
  constructor(){
    super();
    this.state = {myData: []}
  }
  render() {
    return(
      <div className="demo-card-square mdl-card mdl-shadow--2dp">
        <div className="mdl-card__title mdl-card--expand">
          <h2 className="mdl-card__title-text">Write a Blog</h2>
        </div>
        <div className="mdl-card__supporting-text">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          Aenan convallis.
        </div>
        <div className="mdl-card__actions mdl-card--border">
          <a className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" href="/newpost">
            Start Writing
          </a>
        </div>
      </div>
  );
  }
}

ReactDOM.render(
  <InfoTab />,
  document.getElementById('info')
)
