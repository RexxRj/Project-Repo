const mongoose = require("mongoose");
const HttpError = require("./http-error");
//const uniqueValidator = require("mongoose-unique-validator");

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true, minlength: 6 },
  image: { type: String, required: true },
  places: [{ type: mongoose.Types.ObjectId, required: true, ref: "Place" }],
});

//userSchema.plugin(uniqueValidator); This method is deprecated for mongoose v8+.

userSchema.post("save", (error, doc, next) => {
  if (error.name === "MongoServerError" && error.code === 11000) {
    next(new HttpError(`${Object.keys(error.keyValue)} must be unique`, 422));
  } else {
    next(error);
  }
});

module.exports = mongoose.model("User", userSchema);
