const express = require('express');  // import Express Server API

const router = express.Router();     // build Router

router.get("/", (req, res) => {      // HTTP request and response
    res.send("Server Running !!!");
})

module.exports = router;