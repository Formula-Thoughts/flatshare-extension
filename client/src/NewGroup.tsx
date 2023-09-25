import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { SelectGroupProps } from "./SelectGroup";
import { useFlats } from "./context/FlatsContext";

export const NewGroup = (props: SelectGroupProps) => {
  const { setGroupCode, getGroupCode } = useFlats();
  const [groupCode, setCurrentGroupCode] = useState<string | undefined>(
    undefined
  );

  const { Block, Button } = props;
  const navigate = useNavigate();

  const createNewGroup = () => {
    const url = "https://gbjrcfuc7b.execute-api.eu-west-2.amazonaws.com/groups";

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Calling POST groups", data);
        setGroupCode(data.code);
        navigate("/Flats");
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
      });
  };
  useEffect(() => {
    const fetchGroupCode = async () => {
      const code = await getGroupCode();
      setCurrentGroupCode(code || "");
    };
    fetchGroupCode();
  }, [getGroupCode]);

  if (groupCode) {
    return (
      <Block>
        <p>
          You are already part of a group. Share your group code with your
          flatmates to start sharing links.
        </p>
        <Button onClick={() => navigate("/Flats")}>Go to your group</Button>
      </Block>
    );
  }

  return (
    <Block>
      <p>
        Create a group with your flatmates and start sharing links to find your
        next flat.
      </p>
      <Button onClick={createNewGroup}>Create a new group</Button>
    </Block>
  );
};
