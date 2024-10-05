import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import styled from "styled-components";
import { useProvider } from "../context/AppProvider";
import { Button, InputText, Text, TextTypes } from "flatini-fe-library";
import { FaCheck } from "react-icons/fa";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const InputGroup = styled.div`
  flex-direction: column;
  display: flex;
  gap: 1rem;
`;

const Settings = () => {
  const { updateRequirements, requirements } = useProvider();
  const [settingsSaved, setSettingsSaved] = useState<boolean | null>(null);

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
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "1rem",
              marginBottom: "2rem",
            }}
          >
            <InputGroup>
              <label style={{ display: "block", opacity: 0.5 }}>
                Max price per month (£)
              </label>
              <div style={{ display: "flex", alignItems: "center" }}>
                <InputText
                  type="text"
                  name="price"
                  placeholder="Set a max price (PCM)"
                  value={localRequirements.price as string}
                  style={{ width: "100%" }}
                  onChange={(value) =>
                    setLocalRequirements({ ...localRequirements, price: value })
                  }
                />
              </div>
            </InputGroup>
            <InputGroup>
              <label style={{ display: "block", opacity: 0.5 }}>
                Desired locations (Use commas to add multiple)
              </label>
              <div style={{ display: "flex", alignItems: "center" }}>
                <InputText
                  type="text"
                  name="location"
                  placeholder="Set desired locations..."
                  value={localRequirements.locations.join(", ")}
                  style={{ width: "100%" }}
                  onChange={(value) =>
                    setLocalRequirements({
                      ...localRequirements,
                      locations: value.split(",").map((s) => s.trim()),
                    })
                  }
                />
              </div>
            </InputGroup>
          </div>
          <Button
            onClick={async () => {
              await updateRequirements(
                localRequirements.price,
                localRequirements.locations
              );
              setSettingsSaved(true);

              setTimeout(() => {
                setSettingsSaved(null);
              }, 1500);
            }}
            label="Save settings"
          />
          {settingsSaved ? (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "1rem",
                marginTop: "1.5rem",
              }}
            >
              <FaCheck />
              <Text type={TextTypes.paragraph}>
                Your settings have been saved!
              </Text>
            </div>
          ) : null}
        </form>
      </Wrapper>
    </MainLayout>
  );
};

export default Settings;
