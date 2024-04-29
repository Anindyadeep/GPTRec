/* eslint-disable react/prop-types */
import { useState } from 'react';
import { postRecommend } from '../../apis/apis';

function SearchBox({ recommendation, setRecommendation }) {
  const [movieInput, setMovieInput] = useState('');

  const handleInputChange = (e) => {
    setMovieInput(e.target.value);
  };

  const handleRecommend = async () => {
    if (movieInput) {
      const output = await postRecommend({
        "text": movieInput
      })
      console.log(output)
      setRecommendation(output)
    } else {
      setRecommendation([])
    }
  };

  return (
    <div className="w-full">
      <div className="bg-transparent rounded-lg flex flex-row align-center p-6 max-w-xl h-auto " style={{ margin: '200px auto' }}>
        <input
          type="text"
          value={movieInput}
          onChange={handleInputChange}
          className="border border-gray-300 rounded-full p-5 w-full break-normal text-lg "
        />
        <button
          onClick={handleRecommend}
          className="bg-blue-500 text-white rounded-full p-5 w-small break-normal text-lg hover:bg-blue-600 transition-colors duration-300"
        >
          recommend
        </button>
      </div>
    </div>
  );
};

export default SearchBox;