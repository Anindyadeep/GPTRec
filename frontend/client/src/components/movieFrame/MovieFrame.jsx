import React from 'react'
import '../../App.css'
import { LazyLoadImage } from 'react-lazy-load-image-component'
import noPoster from "../../assets/no-poster.png";
function MovieFrame(props) {
  return (
    <div style={{}} >
      <div >
        <div style={{}} />
        <LazyLoadImage
          style={{ objectFit: "cover" }}
          width={"200"} height={"250"}
          alt=""
          effect="blur"
          src={props?.poster || noPoster}
        />
      </div>
      <div style={{ width: "200px", padding: 10, backgroundColor: "white" }}>
        <div style={{ textDecoration: "none", marginBottom: 8, fontWeight: 600, color: "grey", fontSize: 12, fontFamily: "Nunito" }}>

          {props?.item.year}
        </div>
        <div style={{ height: 30, fontWeight: 700, fontSize: 18, fontFamily: "Nunito", color: "grey", }}>
          {props?.item.title.length > 30 ? props?.item.title.slice(0, 30) + "..." : props?.item.title}

        </div>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 5, fontWeight: 700, fontSize: 18, fontFamily: "Nunito" }}>
          <div style={{ display: "flex", flexDirection: "row", alignItems: "center", }}>
            <span className="material-symbols-outlined orange-200">
              star
            </span>
            <div style={{ fontWeight: 400, color: "black", fontSize: 14, fontFamily: "Nunito" }}>
              {props?.item.rating}/10
            </div>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "row", alignItems: "center", paddingBottom: 8, fontWeight: 600, color: "grey", fontSize: 12, fontFamily: "Nunito" }}>
          {
            props?.item.genres.map((item, index) => {
              if (index < 3)
                return (<span style={{ textTransform: "capitalize", marginRight: 4, color: "grey", }}> {item} </span>)
            })
          }
        </div>
      </div>
    </div >
  )
}

export default MovieFrame