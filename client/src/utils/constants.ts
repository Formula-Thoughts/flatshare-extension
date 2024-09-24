export const flatiniAuthWebsite =
  process.env.NODE_ENV === "production"
    ? process.env.REACT_APP_FRONTEND_URL_PROD
    : process.env.REACT_APP_FRONTEND_URL_STAGING;
