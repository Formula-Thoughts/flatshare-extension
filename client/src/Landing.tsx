import { useNavigate } from "react-router-dom";
import { SelectGroup } from "./SelectGroup";
import { useEffect, useState } from "react";

export const Landing = () => {
  const navigate = useNavigate();
  const [whichGroup, setWhichGroup] = useState(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    chrome.storage.local.get("groupSelected", function (result) {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      } else {
        if (result?.groupSelected) {
          setWhichGroup(result.groupSelected);
        }
        setIsLoading(false);
      }
    });
  }, []);

  if (isLoading) {
    return <div>...</div>;
  }

  if (whichGroup) {
    navigate("/Flats");
    return <div>Redirecting to {whichGroup} !</div>;
  }

  return <SelectGroup />;
};
