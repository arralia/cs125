import axios from "axios";
import { useState, useEffect } from "react";

// apiCall function to componentize the api posts
export default function useApiPost({ api }) {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  // This is the "execute" function you call in your onSubmit
  // the way this works is that it will create a execute funciton for you
  // that you can call in what ever way you need later, so it doesnt just automatically run
  // when the component mounts
  const execute = async (data) => {
    setLoading(true);
    try {
      console.log("API Call:", api);
      const res = await axios.post(api, data);
      setResponse(res.data);
      return res.data; // Return it so 'await' can catch it
    } catch (err) {
      console.error("API Error:", err);
      throw err; // Throw it so the form can show an error
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, response };
}
