import axios from 'axios';
import { useState, useEffect } from 'react';


// apiCall function to componentize the api calls 
export default function useApiCall({ api }) {
    const [data, setData] = useState(null);

    useEffect(() => {
        axios.get(api)
            .then(res => setData(res.data))
            .catch(err => console.error(err));
    }, [api]);
    console.log("calling api, here's the data: ", data);
    return data;
}