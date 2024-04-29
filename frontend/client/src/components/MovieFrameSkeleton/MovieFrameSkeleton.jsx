import React from 'react'
import "./style.css"
export default function MovieFrameSkeleton() {
	return (

		<div className="card is-loading">
			<div className="image"></div>
			<div className="content">
				<h2></h2>
				<p></p>
			</div>
		</div>
	)
}
