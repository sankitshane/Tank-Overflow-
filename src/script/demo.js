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

  renderList() {
    return  this.state.myData.map((item) => {
      return (
            <div key={item._id.$oid}>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
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
