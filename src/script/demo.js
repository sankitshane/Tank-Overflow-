import React from 'react';
import ReactDOM from 'react-dom';

class NewComponent extends React.Component {
  constructor(props){
    super(props);
    this.state = {myData: []}
  }

  componentWillMount(){
    let data = document.getElementById('demo').innerHTML;
    data = JSON.parse(data);
    this.setState({myData: data});
  }

  render_tags(tags) {
    return tags.map((tag) => {
      return (
        <span className="mdl-chip">
          <span className="mdl-chip__text">{tag}</span>
        </span>
      );
    });
  }

  render_string(str){
    if (str.length > 350){
      return(
        <div className="mdl-card__supporting-text">
          {str.substring(0,350)+ "........."}
        </div>
      );
    }
    else {
      return(
        <div className="mdl-card__supporting-text">
          {str+"."}
        </div>
      );
    }
  }

  renderList() {
    return  this.state.myData.map((item) => {
      return (
            <div className="demo-card-wide mdl-card mdl-shadow--2dp" key={item._id.$oid}>
              <div className="mdl-card__title">
                <h2 className="mdl-card__title-text">{item.title}</h2>
                <div className="mdl-layout-spacer"></div>
                <div className="tags">
                  {this.render_tags(item.tags)}
              </div>
              </div>
              {this.render_string(item.description)}
              <div className="mdl-card__menu">
                <button className="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">
                  <i className="material-icons">share</i>
                </button>
              </div>
            </div>
        );
      });
    }

  render() {
    if(this.state.myData.length){
      return <div>{this.renderList()}</div> }
    else
      return <div>Loading...</div>
  }
}


ReactDOM.render(
  <NewComponent />,
  document.getElementById('demo')
)
