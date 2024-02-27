import React from "react";
import { flatiniAuthWebsite } from "../utils/constants";

const Auth = () => {
  return (
    <div>
      Auth.{" "}
      <div>
        Click{" "}
        <a href={flatiniAuthWebsite} target="_blank">
          here
        </a>
        to authenticate
      </div>
    </div>
  );
};

export default Auth;
