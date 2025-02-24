const HttpError = require("../models/http-error");

const DUMMY_PLACES = [
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

const getPlaceByUserId = (req, res, next) => {
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

exports.getPlaceById = getPlaceById;
exports.getPlaceByUserId = getPlaceByUserId;
