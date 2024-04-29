import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import dayjs from "dayjs";
import Img from "../../components/lazyLoadImage/Img";
import ContentWrapper from "../../components/contentWrapper/ContentWrapper";
import Genres from "../../components/genres/Genres";
import CircleRating from "../../components/circleRating/CircleRating";
import noResult from "../../assets/no-results.png";
import { NavLink } from "react-router-dom";
import MovieFrame from "../../components/movieFrame/MovieFrame";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./style.css";
import MovieFrameSkeleton from "../../components/MovieFrameSkeleton/MovieFrameSkeleton";
import { postRecommend, postWatchHistory } from "../../apis/apis";
import { SampleNextArrow, SamplePrevArrow } from "../home/Home"
function MovieDesc() {
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [similarMovie, setSimilarMovies] = useState({ watch_history: [], recommended: [] });
  const [similarLoader, setSimilarLoader] = useState(true);
  const { id } = useParams();

  const postSimilarMovies = async (movie) => {
    try {
      const res1 = await postWatchHistory({ objs: [movie] });
      const res2 = await postRecommend({ objs: [movie] });
      console.log("res2: ", JSON.stringify(res2))
      const uniqueRes1 = Object.values(res1.reduce((acc, obj) => {
        acc[obj.title] = obj;
        return acc;
      }, {}));

      const uniqueRes2 = Object.values(res2.reduce((acc, obj) => {
        console.log("id is: ", obj._id)
        acc[obj.title] = obj;
        return acc;
      }, {}));


      console.log("res1 and 2 in similar movies:", uniqueRes1, uniqueRes2);
      setSimilarMovies({ watch_history: uniqueRes1.filter((res) => res._id !== movie._id), recommended: uniqueRes2.filter((res) => res._id !== movie._id) });

      setSimilarLoader(false);
    } catch (err) {
      console.log("error:", err);
    }
  }



  console.log("similar movies:".similarMovie);
  useEffect(() => {
    const fetchData = async () => {

      try {
        const response = await axios.get(`https://8328-203-192-244-29.ngrok-free.app/api/v1/movie/${id}`);
        console.log("res in movie desc:", response.data);
        setMovie(response.data);
        await postSimilarMovies(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching movie:", error);
        setLoading(false);
      }
    }
    fetchData();
  }, [id]);

  const toHoursAndMinutes = (totalMinutes) => {
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    return `${hours}h${minutes > 0 ? ` ${minutes}m` : ""}`;
  };

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
    <div >
      <div className="movieDescription">
        {!loading ? (
          movie ? (
            <ContentWrapper>
              <div className="content">
                <div className="left">
                  <Img className="posterImg" src={movie.poster} />
                </div>
                <div className="right">
                  <div className="title">
                    {movie.title} ({movie.year})
                  </div>

                  <Genres data={movie.genres} />

                  <div className="row">
                    <CircleRating rating={movie.imdb.rating.toFixed(1)} />
                  </div>

                  <div className="overview">
                    <div className="heading">Overview</div>
                    <div className="fullplot">{movie.fullplot}</div>
                  </div>

                  <div className="info">
                    {movie.languages && (
                      <div className="infoItem">
                        <span className="text bold">Language(s): </span>
                        <span className="text">
                          {movie.languages.map((lang, index) => (
                            <span key={index}>
                              {lang}
                              {index !== movie.languages.length - 1 && ", "}
                            </span>
                          ))}
                        </span>
                      </div>
                    )}

                    {movie.released && (
                      <div className="infoItem">
                        <span className="text bold">Release Date: </span>
                        <span className="text">
                          {dayjs(movie.released.$date).format("MMM D, YYYY")}
                        </span>
                      </div>
                    )}

                    {movie.runtime && (
                      <div className="infoItem">
                        <span className="text bold">Runtime: </span>
                        <span className="text">
                          {toHoursAndMinutes(movie.runtime)}
                        </span>
                      </div>
                    )}
                  </div>

                  {movie.directors && (
                    <div className="info">
                      <span className="text bold">Director(s): </span>
                      <span className="text">
                        {movie.directors.map((direct, index) => (
                          <span key={index}>
                            {direct}
                            {index !== movie.directors.length - 1 && ", "}
                          </span>
                        ))}
                      </span>
                    </div>
                  )}

                  {movie.writers && (
                    <div className="info">
                      <span className="text bold">Writer(s): </span>
                      <span className="text">
                        {movie.writers.map((write, index) => (
                          <span key={index}>
                            {write}
                            {index !== movie.writers.length - 1 && ", "}
                          </span>
                        ))}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </ContentWrapper>
          ) : (
            <div className="noMovieContainer">
              <img src={noResult} alt="No Movie" className="resultNotFound" />
            </div>
          )
        ) : (
          <div className="movieDescriptionSkeleton">
            <ContentWrapper>
              <div className="left skeleton"></div>
              <div className="right">
                <div className="row skeleton"></div>
                <div className="row skeleton"></div>
                <div className="row skeleton"></div>
                <div className="row skeleton"></div>
                <div className="row skeleton"></div>
                <div className="row skeleton"></div>
                <div className="row skeleton"></div>
              </div>
            </ContentWrapper>
          </div>
        )}
      </div>
      {similarLoader || similarMovie.watch_history.length > 0 && <h1 style={{ marginBottom: 30, paddingLeft: 100 }}>Similar Movies you would like</h1>}
      {similarLoader && similarMovie.watch_history.length > 0 ?
        <div style={{ display: "flex", flexDirection: "row", flexWrap: "wrap", paddingLeft: 100 }}>
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />

        </div>
        :
        <div style={{ display: "flex", flexDirection: "row", flexWrap: "wrap", paddingLeft: 100 }} className="movie-list" >
          {similarMovie.watch_history.map((movie) => (
            <NavLink className="no-underline" style={{ textDecoration: 'none', width: 230 }} to={`/movie/${movie._id}`} key={movie._id}>
              <MovieFrame poster={movie.poster} item={movie} />
            </NavLink>
          ))}
        </div>
      }

      {similarLoader || similarMovie.recommended.length > 0 && <h1 style={{ marginBottom: 30, paddingLeft: 100, paddingTop: 50 }}>Similar Movies</h1>}
      {similarLoader && similarMovie.recommended.length > 0 ?
        <div style={{ display: "flex", flexDirection: "row", flexWrap: "wrap", paddingLeft: 100 }}>
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />
          <MovieFrameSkeleton />

        </div>
        :
        <div style={{ display: "flex", flexDirection: "row", flexWrap: "wrap", paddingLeft: 100 }} className="movie-list" >

          {similarMovie.recommended.map((movie) => (
            <NavLink className="no-underline" style={{ textDecoration: 'none', width: 230 }} to={`/movie/${movie._id}`} key={movie._id}>
              <MovieFrame poster={movie.poster} item={movie} />
            </NavLink>
          ))}


        </div>
      }

    </div>)
}

export default MovieDesc;
