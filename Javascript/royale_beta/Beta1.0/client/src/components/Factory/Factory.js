import User1 from './User1'
import User2 from './User2'
import Wall1 from './Wall1'

function Factory(props) {
    switch (props.component) {
      case "z":
        return <User1 data = {props.data}/>;
      case "x":
        return <User2 data = {props.data} />;
      case "w":
        return <Wall1 data = {props.data} />;
      default:
        return null;
    }
}

export default Factory;