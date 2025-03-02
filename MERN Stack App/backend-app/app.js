const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");

const placesRoutes = require("./routes/places-routes");
const usersRoutes = require("./routes/users-routes");
const HttpError = require("./models/http-error");

const url =
  "mongodb+srv://rexxogrator:GxlP4dyJdrma615a@cluster0.0tevh.mongodb.net/places?retryWrites=true&w=majority&appName=Cluster0";

const app = express();

app.use(bodyParser.json());

app.use("/api/places", placesRoutes);
app.use("/api/users", usersRoutes);

app.use((req, res, next) => {
  const error = new HttpError("Could not find this route.", 404);
  throw error;
});

app.use((error, req, res, next) => {
  if (res.headerSent) {
    return next(error);
  }

  res.status(error.code || 500);
  res.json({ message: error.message || "An unknown error occurred!" });
});

mongoose
  .connect(url)
  .then(() => {
    console.log("Connected to the database!");
    app.listen(5000);
  })
  .catch((err) => {
    console.log(err);
  });
