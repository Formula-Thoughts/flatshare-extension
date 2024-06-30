import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import InputText from "../flatini-library/components/InputText";
import styled from "styled-components";
import { useProvider } from "../context/AppProvider";
import Button from "../flatini-library/components/Button";
import Text, { TextTypes } from "../flatini-library/components/Text";
import { FaEdit } from "react-icons/fa";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
        <div
          style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}
        >
          <Text type={TextTypes.title}>Settings</Text>
          <Text type={TextTypes.small}>Set your flat requirements</Text>
        </div>
        <form onSubmit={(e) => e.preventDefault()}>
          <div>
            <label style={{ display: "block", opacity: 0.5 }}>
              Max price per month (£)
            </label>
            <div style={{ display: "flex", alignItems: "center" }}>
              <InputText
                type="text"
                name="price"
                placeholder="Set a max price (PCM)"
                value={localRequirements.price as string}
                defaultValue={localRequirements.price as string}
                onChange={(value) =>
                  setLocalRequirements({ ...localRequirements, price: value })
                }
              />
              <FaEdit size={30} style={{ opacity: 0.5 }} />
            </div>
          </div>
          <div>
            <label style={{ display: "block", opacity: 0.5 }}>
              Desired locations (Use commas to add multiple)
            </label>
            <div style={{ display: "flex", alignItems: "center" }}>
              <InputText
                type="text"
                name="location"
                placeholder="Set desired locations..."
                value={localRequirements.locations.join(", ")}
                defaultValue={localRequirements.locations.join(", ")}
                onChange={(value) =>
                  setLocalRequirements({
                    ...localRequirements,
                    locations: value.split(",").map((s) => s.trim()),
                  })
                }
              />
              <FaEdit size={30} style={{ opacity: 0.5 }} />
            </div>
          </div>
          <Button
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
