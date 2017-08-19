import React from 'react';
import ReactDOM from 'react-dom';

class NewComponent extends React.Component {
  constructor(props){
    super(props);
    this.state = {myData: {}}
  }

  componentDidMount(){
    let data = document.getElementById('demo').InnerHTML;
    data = JSON.parse(data);
    this.setState({myData: data});
  }

  render(){
    return(
      let now_data = this.state.mydata
      <h2>{now_data}</h2>
    );
  }
}


ReactDOM.render(
  <NewComponent />,
  document.getElementById('demo')
)
