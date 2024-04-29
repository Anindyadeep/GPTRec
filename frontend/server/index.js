require('dotenv').config();

const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const { ObjectId } = require("mongodb");

const app = express();
app.use(express.json());
app.use(cors());

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(
      `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@moviecluster.aodx1qo.mongodb.net/sample_mflix?retryWrites=true&w=majority&appName=MovieCluster`
    );
    console.log("DB Connected");
  } catch (error) {
    console.error("MongoDB connection error:", error);
    process.exit(1);
  }
};

connectDB();

const movieSchema = new mongoose.Schema({
  title: String,
  poster: String,
  plot: String,
  fullplot: String,
  year: Number,
  imdb: Object,
  cast: Array,
});

const Movie = mongoose.model("embedded_movies", movieSchema);

app.get("/", async (req, res) => {
  try {
    const movies = await Movie.find();
    return res.json({ movies });
  } catch (error) {
    console.error("Error fetching movies:", error);
    res.status(500).json({ error: "Server error" });
  }
});

app.get("/movie/:id", async (req, res) => {
  try {
    const movie = await Movie.findById(req.params.id);
    if (!movie) {
      return res.status(404).json({ error: "Movie not found" });
    }
    return res.json({ movie });
  } catch (error) {
    console.error("Error fetching movie by ID:", error);
    res.status(500).json({ error: "Server error" });
  }
});

const PORT = 3000;

const server = app.listen(PORT, () => {
  console.log(`App is live on port ${PORT}`);
});

server.on("error", (error) => {
  console.error("Server startup error:", error);
  process.exit(1);
});
