import User1 from './User1'
import User2 from './User2'

function Factory(props) {
    switch (props.component) {
      case "z":
        return <User1 />;
      case "x":
        return <User2 />;
      default:
        return null;
    }
}

export default Factory;