const CLIENT_URL = process.env.CLIENT_URL || 'http://localhost';
const CLIENT_PORT = process.env.CLIENT_PORT || 3000;
const SERVER_URL = process.env.SERVER_URL || 'http://localhost';
const SERVER_PORT = process.env.SERVER_PORT || 5000;

module.exports = {
    'SERVER_URL': SERVER_URL,
    'SERVER_PORT': SERVER_PORT,
    'CLIENT_URL': CLIENT_URL,
    'CLIENT_PORT': CLIENT_PORT,
}