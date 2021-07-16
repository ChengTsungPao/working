const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.send(`Server has started on port ${process.env.SERVER_PORT}`);
});

module.exports = router;