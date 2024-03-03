import React from "react";
import Button from "../flatini-library/components/Button";
import { useProvider } from "../context/AppProvider";

const CreateGroup = () => {
  const { createGroup } = useProvider();

  return (
    <div>
      CreateGroup
      <div>
        <Button onClick={createGroup} label="Add to the list anyway" />
      </div>
    </div>
  );
};

export default CreateGroup;
