import React, { useCallback } from "react";

import Input from "../../shared/components/FormElements/Input";
import "./NewPlace.css";
import {
  VALIDATOR_MINLENGTH,
  VALIDATOR_REQUIRE,
} from "../../shared/util/validators";

const NewPlace = () => {
  const titleInputHandler = useCallback((id, value, isValid) => {}, []);
  const descriptionInputHandler = useCallback((id, value, isValid) => {}, []);

  return (
    <form className="place-form">
      <Input
        id="title"
        element="input"
        type="text"
        label="Title"
        validators={[VALIDATOR_REQUIRE()]}
        errorText="Please enter a valid Title!"
        onInput={titleInputHandler}
      />
      <Input
        id="description"
        element="textarea"
        label="Description"
        validators={[VALIDATOR_MINLENGTH(5)]}
        errorText="Please enter a valid Description (at least 5 characters)!"
        onInput={descriptionInputHandler}
      />
    </form>
  );
};

export default NewPlace;
