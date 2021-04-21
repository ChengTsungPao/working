import User1 from './User1'
import User2 from './User2'

function Factory(props) {
    switch (props.component) {
      case "z":
        return <User1 data = {props.data}/>;
      case "x":
        return <User2 data = {props.data} />;
      default:
        return null;
    }
}

export default Factory;