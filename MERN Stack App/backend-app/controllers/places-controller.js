const { v4: uuidv4 } = require("uuid");
const { validationResult } = require("express-validator");
const HttpError = require("../models/http-error");

const getCoordsForAddress = require("../util/location");

let DUMMY_PLACES = [
  {
    id: "p1",
    title: "Gandhi Mandap",
    imageURL:
      "https://lh5.googleusercontent.com/p/AF1QipO5mAyigddIiLZh31pazcmCRvgRIA9vxWkD6Fpx=w408-h543-k-no",
    desc: "Hilltop monument with an Indian flag & marble statue honoring civil-rights activist Mahatma Gandhi.",
    address: "Ulubari, Sarania Hills, Guwahati, Assam 781007",
    creator: "u1",
    location: {
      lat: "26.177389",
      lng: "91.768175",
    },
  },
  {
    id: "p2",
    title: "Maa Kamakhya Temple",
    imageURL:
      "https://lh5.googleusercontent.com/p/AF1QipMQvrztkdR0Vik0sgsXkb0zzhFYx5o11CUcUNGU=w408-h306-k-no",
    desc: "Hilltop, Hindu temple complex with distinctive domed roofs, originally dating from the 7th century.",
    address: "Kamakhya, Guwahati, Assam 781010",
    creator: "u2",
    location: {
      lat: "26.1695645",
      lng: "91.6982519",
    },
  },
  {
    id: "p3",
    title: "Maa Kamakhya Temple",
    imageURL:
      "https://lh5.googleusercontent.com/p/AF1QipMQvrztkdR0Vik0sgsXkb0zzhFYx5o11CUcUNGU=w408-h306-k-no",
    desc: "Hilltop, Hindu temple complex with distinctive domed roofs, originally dating from the 7th century.",
    address: "Kamakhya, Guwahati, Assam 781010",
    creator: "u1",
    location: {
      lat: "26.1695645",
      lng: "91.6982519",
    },
  },
];

const getPlaceById = (req, res, next) => {
  const placeId = req.params.pid;
  const place = DUMMY_PLACES.find((p) => {
    return p.id === placeId;
  });

  if (!place) {
    throw new HttpError("Could not find a place for the provided id.", 404);
  }

  res.json({ place });
};

const getPlacesByUserId = (req, res, next) => {
  const userId = req.params.uid;
  const places = DUMMY_PLACES.filter((p) => {
    return p.creator === userId;
  });

  if (!places || places.length === 0) {
    return next(
      new Error("Could not find a place for the provided user id.", 404)
    );
  }

  res.json({ places });
};

const createPlace = async (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    console.log(errors);
    return next(
      new HttpError("Invalid inputs passed, please check your data", 422)
    );
  }

  const { title, desc, address, creator } = req.body;

  let coordinates;
  try {
    coordinates = await getCoordsForAddress(address);
  } catch (error) {
    return next(error);
  }

  const createdPlace = {
    id: uuidv4(),
    title,
    desc,
    address,
    creator,
    location: coordinates,
  };

  DUMMY_PLACES.push(createdPlace); //unshift(createdPlace) to add at the beginning of the array

  res.status(201).json({ place: createdPlace });
};

const updatePlace = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    console.log(errors);
    throw new HttpError("Invalid inputs passed, please check your data", 422);
  }
  const { title, desc } = req.body;
  const placeId = req.params.pid;

  const updatedPlace = { ...DUMMY_PLACES.find((p) => p.id === placeId) }; //creates a copy instead of referencing original object
  const placeIndex = DUMMY_PLACES.findIndex((p) => p.id === placeId);
  updatedPlace.title = title;
  updatedPlace.desc = desc;

  DUMMY_PLACES[placeIndex] = updatedPlace;

  res.status(200).json({ place: updatedPlace });
};

const deletePlace = (req, res, next) => {
  const placeId = req.params.pid;
  if (!DUMMY_PLACES.find((p) => p.id === placeId)) {
    throw new HttpError("Could not find a place for that id", 404);
  }

  DUMMY_PLACES = DUMMY_PLACES.filter((p) => p.id !== placeId);
  res.status(200).json({ message: "Deleted place." });
};

exports.getPlaceById = getPlaceById;
exports.getPlacesByUserId = getPlacesByUserId;
exports.createPlace = createPlace;
exports.updatePlace = updatePlace;
exports.deletePlace = deletePlace;
