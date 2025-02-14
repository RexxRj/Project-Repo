import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom/cjs/react-router-dom.min";

import Input from "../../shared/components/FormElements/Input";
import Button from "../../shared/components/FormElements/Button";
import {
  VALIDATOR_REQUIRE,
  VALIDATOR_MINLENGTH,
} from "../../shared/util/validators";
import { useForm } from "../../shared/hooks/form-hook";
import Card from "../../shared/components/UIElements/Card";

import "./PlaceForm.css";

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

const UpdatePlace = () => {
  const [isLoading, setIsLoading] = useState(true);
  const placeId = useParams().placeId;
  const [formState, inputHandler, setFormData] = useForm(
    {
      title: {
        value: "",
        isValid: false,
      },
      description: {
        value: "",
        isValid: false,
      },
    },
    false
  );

  const identifiedPlace = DUMMY_PLACES.find((p) => p.id === placeId);

  useEffect(() => {
    if (identifiedPlace) {
      setFormData(
        {
          title: {
            value: identifiedPlace.title,
            isValid: true,
          },
          description: {
            value: identifiedPlace.desc,
            isValid: true,
          },
        },
        true
      );
    }
    setIsLoading(false);
  }, [setFormData, identifiedPlace]);

  const placeUpdateSubmitHandler = (event) => {
    event.preventDefault();
    console.log(formState.inputs);
  };

  if (!identifiedPlace) {
    return (
      <div className="center">
        <Card>
          <h2>Could not find place!</h2>
        </Card>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="center">
        <h2>Loading...</h2>
      </div>
    );
  }

  return (
    <form className="place-form" onSubmit={placeUpdateSubmitHandler}>
      <Input
        id="title"
        element="input"
        type="text"
        label="Title"
        validators={[VALIDATOR_REQUIRE()]}
        errorText="Please enter a valid title."
        onInput={inputHandler}
        initialValue={formState.inputs.title.value}
        initialIsValid={formState.inputs.title.isValid}
      />
      <Input
        id="description"
        element="textarea"
        label="Description"
        validators={[VALIDATOR_MINLENGTH(5)]}
        errorText="Please enter a valid description (min. 5 characters)."
        onInput={inputHandler}
        initialValue={formState.inputs.description.value}
        initialIsValid={formState.inputs.description.isValid}
      />
      <Button type="submit" disabled={!formState.isValid}>
        UPDATE PLACE
      </Button>
    </form>
  );
};

export default UpdatePlace;
