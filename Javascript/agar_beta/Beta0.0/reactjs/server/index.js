const SOCKET = require('./utils/socket');
const constants = require('./utils/globalVariable/constants');
const logger = require('./utils/functions/logger');


SOCKET.SERVER.listen(constants.SERVER_PORT, () => {
    console.log(`Server has started on port ${constants.SERVER_PORT}`)
    logger.debug(`Server has started on port ${constants.SERVER_PORT}`)
});
