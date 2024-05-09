import axios from "axios";

export default axios.create({
  baseURL:
    process.env.REACT_APP_API_URL ||
    "https://pmer135n4j.execute-api.eu-west-2.amazonaws.com",
  timeout: 10000,
});
