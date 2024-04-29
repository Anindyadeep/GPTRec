import React from 'react'

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
  