import React from "react";
import MainLayout from "../layouts/MainLayout";
import InputText from "../dwelly-library/components/InputText";
import styled from "styled-components";
import { useFlats } from "../context/AppProvider";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
`;

const Settings = () => {
  const { requirements, setRequirements } = useFlats();
  return (
    <MainLayout>
      <Wrapper>
        <div>Settings</div>

        <form>
          <div>
            <label style={{ display: "block" }}>Price</label>
            <InputText
              type="text"
              name="price"
              placeholder="Price"
              value={requirements.price}
              onChange={(value) =>
                setRequirements({ ...requirements, price: value })
              }
            />
          </div>
          <div>
            <label style={{ display: "block" }}>Location</label>
            <InputText
              type="text"
              name="location"
              placeholder="Location"
              value={requirements.location.join(", ")}
              onChange={(value) =>
                setRequirements({
                  ...requirements,
                  location: value.split(",").map((s) => s.trim()),
                })
              }
            />
          </div>
          {/* <InputText
            type="text"
            name="location"
            placeholder="Price"
            value={requirements.price}
            onChange={(value) =>
              setRequirements({ ...requirements, price: value })
            }
          /> */}
        </form>
      </Wrapper>
    </MainLayout>
  );
};

export default Settings;
