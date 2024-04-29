import React from 'react'
// import {BASE_URL} from "../../.env"
import axios from "axios";

const BASE_URL = "https://8328-203-192-244-29.ngrok-free.app"

export const postWatchHistory = async (body) => {
    try {
        const res = await axios.post(BASE_URL + "/api/v1/watch_history_recommend", body);
        console.log("res in watch_history_recommend:", res.data.search_results.result);
    } catch (e) {
        console.log("error:", e);
        return []
    }
}

export const postRecommend = async (body) => {
    try {
        console.log("---------", body)
        const res = await axios.post(BASE_URL + "/api/v1/recommend", body);
        console.log("res in postRecommend:", res.data.search_results.result);
        return res.data.search_results.result
    } catch (e) {
        console.log("error:", e);
        return []
    }
}
