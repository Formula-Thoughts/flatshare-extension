import axios from "axios";

export default axios.create({
  baseURL:
    process.env.NODE_ENV === "production"
      ? process.env.REACT_APP_BACKEND_URL_PROD
      : process.env.REACT_APP_BACKEND_URL_STAGING,
  timeout: 10000,
});
