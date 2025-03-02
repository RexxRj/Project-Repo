const { v4: uuidv4 } = require("uuid");
const { validationResult } = require("express-validator");
const HttpError = require("../models/http-error");

const getCoordsForAddress = require("../util/location");
const Place = require("../models/place");

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

const getPlaceById = async (req, res, next) => {
  const placeId = req.params.pid;

  let place;
  try {
    place = await Place.findById(placeId);
  } catch (err) {
    const error = new HttpError(
      "Something went wrong, could not find a place",
      500
    );
    return next(error);
  }

  if (!place) {
    const error = new HttpError(
      "Could not find a place for the provided id.",
      404
    );
    return next(error);
  }

  res.json({ place: place.toObject({ getters: true }) });
};

const getPlacesByUserId = async (req, res, next) => {
  const userId = req.params.uid;
  let places;

  try {
    places = await Place.find({ creator: userId });
  } catch (err) {
    const error = new HttpError(
      "Fetching places failed, please try again later",
      500
    );
    return next(error);
  }

  if (!places || places.length === 0) {
    return next(
      new HttpError("Could not find a place for the provided user id.", 404)
    );
  }

  res.json({
    places: places.map((place) => place.toObject({ getters: true })),
  });
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

  const createdPlace = new Place({
    title,
    desc,
    address,
    creator,
    location: coordinates,
    image:
      "https://lh5.googleusercontent.com/p/AF1QipMQvrztkdR0Vik0sgsXkb0zzhFYx5o11CUcUNGU=w408-h306-k-no",
  });

  try {
    await createdPlace.save();
  } catch (err) {
    const error = new HttpError("Creating place failed, please try again", 500);
    return next(error);
  }

  res.status(201).json({ place: createdPlace });
};

const updatePlace = async (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    console.log(errors);
    throw new HttpError("Invalid inputs passed, please check your data", 422);
  }
  const { title, desc } = req.body;
  const placeId = req.params.pid;

  let place;
  try {
    place = await Place.findById(placeId);
  } catch (err) {
    const error = new HttpError(
      "Something went wrong, could not update place",
      500
    );
    return next(error);
  }

  place.title = title;
  place.desc = desc;

  try {
    await place.save();
  } catch (err) {
    const error = new HttpError(
      "Something went wrong, could not update place",
      500
    );
    return next(error);
  }

  res.status(200).json({ place: place.toObject({ getters: true }) });
};

const deletePlace = async (req, res, next) => {
  const placeId = req.params.pid;

  try {
    await Place.findByIdAndDelete(placeId);
  } catch (err) {
    const error = new HttpError(
      "Something went wrong, could not delete place",
      500
    );
    return next(error);
  }

  res.status(200).json({ message: "Deleted place." });
};

exports.getPlaceById = getPlaceById;
exports.getPlacesByUserId = getPlacesByUserId;
exports.createPlace = createPlace;
exports.updatePlace = updatePlace;
exports.deletePlace = deletePlace;
