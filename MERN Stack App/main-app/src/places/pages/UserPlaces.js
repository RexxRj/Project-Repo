import React from "react";
import { useParams } from "react-router-dom";

import PlaceList from "../components/PlaceList";

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
];

const UserPlaces = (props) => {
  const userId = useParams().userId;
  const loadedPlaces = DUMMY_PLACES.filter((place) => place.creator === userId);
  return <PlaceList items={loadedPlaces} />;
};

export default UserPlaces;
