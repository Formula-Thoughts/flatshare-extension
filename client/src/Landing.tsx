import { useNavigate } from "react-router-dom";
import { SelectGroup } from "./SelectGroup";
import { useEffect, useState } from "react";
import { useFlats } from "./context/FlatsContext";

export const Landing = () => {
  const { getGroupCode } = useFlats();
  const navigate = useNavigate();
  const [groupCode, setGroupCode] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchGroupCode = async () => {
      const code = await getGroupCode();
      setGroupCode(code || "");
    };
    fetchGroupCode();
    setIsLoading(false);
  }, [getGroupCode]);

  if (isLoading) {
    return <div>...</div>;
  }

  if (groupCode) {
    navigate("/Flats");
    return <div>Redirecting to {groupCode} !</div>;
  }

  return <SelectGroup />;
};
