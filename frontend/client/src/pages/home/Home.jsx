import React, { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
import axios from "axios";
import MovieFrame from "../../components/movieFrame/MovieFrame"
import "./style.css";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import SearchBox from "../../components/searchBox/SearchBox"
import Poster from "../../assets/Poster.png"
import MovieFrameSkeleton from "../../components/MovieFrameSkeleton/MovieFrameSkeleton";


export function SampleNextArrow(props) {
  const { className, style, onClick } = props;

  return (
    <div
      className={className}
      style={{ ...style, height: 30, width: 30, borderRadius: 20, paddingTop: 5, marginRight: 20, backgroundColor: "black" }}
      onClick={onClick}
    />
  );
}

export function SamplePrevArrow(props) {
  const { className, style, onClick } = props;
  return (
    <div
      className={className}
      style={{ ...style, height: 30, width: 30, borderRadius: 20, paddingTop: 5, marginRight: 20, backgroundColor: "black" }}
      onClick={onClick}
    />
  );
}

function Home() {
  const [movies, setMovies] = useState([]);
  const [loader, setLoader] = useState(true);
  const [lastestMovies, setLatestMovies] = useState([]);
  const [recommendation, setRecommendation] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("https://8328-203-192-244-29.ngrok-free.app/api/v1/movies?page=1&page_size=20");
        const res2 = await axios.get("https://8328-203-192-244-29.ngrok-free.app/api/v1/movies?page=2&page_size=20");
        console.log("reponse:", response);
        setMovies(response.data);
        setLatestMovies(res2.data);
        setLoader(false);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  var settings = {

    nextArrow: <SampleNextArrow />,
    prevArrow: <SamplePrevArrow />,
    width: 230,
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 5,
    slidesToScroll: 1,
    gap: 15,
    centerMode: false, // Add this line if you don't want center mode
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 5,
          slidesToScroll: 1,
        }
      },

      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
        }
      }
    ]
  };

  return (
    <div>
      <div className="hero" style={{ backgroundImage: `url(${Poster})`, height: 500, justifyContent: "center", alignItems: "center" }}>
        <div style={{ display: "flex", flexDirection: "row", alignItems: "center", padding: 14 }}>
          <span className="material-symbols-outlined">
            live_tv
          </span>
          <div style={{ color: "white", fontSize: 24, }}>MovieBox</div>

        </div>
        <div style={{ width: "100%", justifyContent: "center", alignItems: "center" }}>
          <SearchBox
            recommendation={recommendation}
            setRecommendation={setRecommendation}
          />
        </div>
      </div>


      <div className="home" >
        {recommendation && recommendation.length !== 0 && <h1 style={{ marginTop: 70, marginBottom: 30 }}>Recommend Movies</h1>}
        {(loader) ?

          <div style={{ display: "flex", flexDirection: "row", }}>
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />

          </div> :
          <div className="movie-list" >
            <Slider {...settings}>
              {recommendation.map((movie) => (
                <NavLink className="no-underline" style={{ textDecoration: 'none', width: 230 }} to={`/movie/${movie._id}`} key={movie._id}>
                  <MovieFrame poster={movie.poster} item={movie} />
                </NavLink>
              ))}
            </Slider>

          </div>}
        <h1 style={{ marginBottom: 30, marginTop: 10 }}>Trending Movies</h1>
        {loader ?

          <div style={{ display: "flex", flexDirection: "row", }}>
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />

          </div>
          :
          <div className="movie-list" >
            <Slider {...settings}>
              {
                movies.map((movie) => (
                  <NavLink className="no-underline" style={{ textDecoration: "none" }}
                    to={`/movie/${movie._id}`} key={movie._id}>
                    <MovieFrame poster={movie.poster} item={movie} />
                  </NavLink>
                ))}
            </Slider>

          </div>}

        <h1 style={{ marginTop: 70, marginBottom: 30 }}>Latest Movies</h1>
        {loader ?

          <div style={{ display: "flex", flexDirection: "row", }}>
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />
            <MovieFrameSkeleton />

          </div> :
          <div className="movie-list" >
            <Slider {...settings}>
              {lastestMovies.map((movie) => (
                <NavLink className="no-underline" style={{ textDecoration: 'none', width: 230 }} to={`/movie/${movie._id}`} key={movie._id}>
                  <MovieFrame poster={movie.poster} item={movie} />
                </NavLink>
              ))}
            </Slider>

          </div>}

      </div>
    </div>
  );
}

export default Home;
