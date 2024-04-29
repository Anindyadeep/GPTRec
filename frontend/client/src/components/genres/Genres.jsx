import React from "react";

import "./style.css";

const Genres = ({ data }) => {
  return (
    <div className="genres">
      {data?.map((genre, index) => (
        <div key={index} className="genre">
          {genre}
        </div>
      ))}
    </div>
  );
};

export default Genres;