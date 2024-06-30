import axios from "axios";

export default axios.create({
  baseURL:
    process.env.REACT_APP_API_URL ||
    "https://v17eiwhzph.execute-api.eu-west-2.amazonaws.com",
  timeout: 10000,
});
