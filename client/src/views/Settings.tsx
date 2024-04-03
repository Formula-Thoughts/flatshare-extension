import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import InputText from "../flatini-library/components/InputText";
import styled from "styled-components";
import { useProvider } from "../context/AppProvider";
import Button from "../flatini-library/components/Button";
import Text, { TextTypes } from "../flatini-library/components/Text";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
`;

const Settings = () => {
  const { updateRequirements, requirements } = useProvider();

  const [localRequirements, setLocalRequirements] = useState<{
    price: null | string;
    locations: string[];
  }>(
    requirements ?? {
      price: null,
      locations: [],
    }
  );
  return (
    <MainLayout>
      <Wrapper>
        <Text type={TextTypes.small}>Settings</Text>
        <form onSubmit={(e) => e.preventDefault()}>
          <div style={{ marginTop: "1rem" }}>
            <label style={{ display: "block" }}>Price</label>
            <InputText
              type="text"
              name="price"
              placeholder="Price"
              value={localRequirements.price as string}
              defaultValue={localRequirements.price as string}
              onChange={(value) =>
                setLocalRequirements({ ...localRequirements, price: value })
              }
            />
          </div>
          <div style={{ marginTop: "1rem" }}>
            <label style={{ display: "block" }}>Location</label>
            <InputText
              type="text"
              name="location"
              placeholder="Location"
              value={localRequirements.locations.join(", ")}
              defaultValue={localRequirements.locations.join(", ")}
              onChange={(value) =>
                setLocalRequirements({
                  ...localRequirements,
                  locations: value.split(",").map((s) => s.trim()),
                })
              }
            />
          </div>
          <Button
            style={{ marginTop: "1rem" }}
            onClick={async () =>
              await updateRequirements(
                localRequirements.price,
                localRequirements.locations
              )
            }
            label="Save settings"
          />
        </form>
      </Wrapper>
    </MainLayout>
  );
};

export default Settings;
