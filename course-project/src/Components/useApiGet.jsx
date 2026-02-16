import axios from "axios";
import { useState, useEffect } from "react";

// apiCall function to componentize the api calls
export default function useApiGet({ api }) {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  // This is the "execute" function you call in your onSubmit
  const execute = async (data) => {
    setLoading(true);
    try {
      const res = await axios.get(api, data);
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
