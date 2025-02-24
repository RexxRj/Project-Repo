const express = require("express");

const placesControllers = require("../controllers/places-controller");

const router = express.Router();

router.get("/user/:uid", placesControllers.getPlaceByUserId);

router.get("/:pid", placesControllers.getPlaceById);

module.exports = router;
