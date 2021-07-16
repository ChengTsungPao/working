/**
 * Configurations of logger.
 */
const winston = require('winston');
const date = require('./date')

const myformat = winston.format((data) => {
    let timestamp = new Date().toLocaleTimeString('zh-TW', { timeZone: 'Asia/Taipei', hour12: false })
    let message = data.message;
    data.message = `${timestamp} > ${message}`
    return data
})();

const logger = winston.createLogger({
    'level': 'debug',
    'format': winston.format.combine(
        myformat,
        winston.format.simple(),
    ),
    'transports': [
        new winston.transports.File({ filename: `./logs/debug/${date.getLocalDate()}.txt` })
    ]
});

const debug = (message) => {
    logger.debug(message);
}

module.exports = {
    'debug': debug
}