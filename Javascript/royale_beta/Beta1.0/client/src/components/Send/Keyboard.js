const keyup = {"z": true, "x": true, "w": true}
const keydown = {"ArrowUp": true, "ArrowDown": true, "ArrowLeft": true, "ArrowRight": true}

const Keyboard = (kind, key) => {
    switch (kind) {
        case "keyup":
          return keyup[key];
        case "keydown":
          return keydown[key];
        default:
          return null;
      }
}

export default Keyboard
