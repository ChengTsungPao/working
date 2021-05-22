import User1 from './User1'
import Wall1 from './Wall1'

function Factory(props) {
    switch (props.component) {
      case "User1":
        return <User1 data = {props.data}/>;
      case "Wall1":
        return <Wall1 data = {props.data} />;
      default:
        return null;
    }
}

export default Factory;