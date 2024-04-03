import { useEffect, useState } from "react";
import styled from "styled-components";
import SaveDataButton from "./SaveDataButton";
import { Flat, useProvider } from "./context/AppProvider";
import {
  getFlatDataFromOpenRent,
  getFlatDataFromRightmove,
  getFlatDataFromSpareroom,
  getFlatDataFromZoopla,
} from "./utils/url";
import Text, { TextTypes } from "./flatini-library/components/Text";
import Image from "./flatini-library/components/Image";
import checkmark from "./flatini-library/assets/checkmark.png";
import cross from "./flatini-library/assets/cross.png";
import { extractNumber } from "./utils/util";
import Button from "./flatini-library/components/Button";

const Wrapper = styled.div<{
  isFlatDuplicated: boolean;
  doesFlatMeetRequirements: boolean;
}>`
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  text-align: left;
  padding: 50px 20px;
  background: ${(props) => {
    if (props.isFlatDuplicated) {
      return "#0B0708";
    }
    if (!props.isFlatDuplicated && props.doesFlatMeetRequirements) {
      return "#AF496E";
    }
    if (!props.isFlatDuplicated && !props.doesFlatMeetRequirements) {
      return "#AF496E";
    }
    return "";
  }};
`;

const InfoWrapper = styled.div`
  margin-top: 2rem;
  gap: 1rem;
  display: flex;
  flex-direction: column;
`;

const FlatView = () => {
  const {
    flats,
    addFlat,
    activeUrl,
    checkIfPropertyMeetsRequirements,
    requirements,
    removeFlat,
  } = useProvider();
  const [isFlatDuplicated, setIsFlatDuplicated] = useState(false);
  const [activeFlatData, setActiveFlatData] = useState({
    price: "",
    title: "",
    url: "",
  });
  const checkFlatIsDuplicated = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length > 0) {
        const activeTab = tabs[0];
        if (flats.find((flat: Flat) => flat.url === activeTab.url)) {
          return setIsFlatDuplicated(true);
        }
        return setIsFlatDuplicated(false);
      }
    });
  };

  const removeFlatFromList = () => {
    removeFlat(activeUrl.contents);
    setIsFlatDuplicated(false);
  };

  useEffect(() => {
    checkFlatIsDuplicated();
    if (activeUrl.propertyProvider === "openrent") {
      getFlatDataFromOpenRent(
        activeUrl.tabId,
        activeUrl.contents,
        (title, url, price) => {
          setActiveFlatData({
            price,
            title,
            url,
          });
        }
      );
    } else if (activeUrl.propertyProvider === "spareroom") {
      getFlatDataFromSpareroom(
        activeUrl.tabId,
        activeUrl.contents,
        (title, url, price) => {
          setActiveFlatData({
            price,
            title,
            url,
          });
        }
      );
    } else if (activeUrl.propertyProvider === "zoopla") {
      getFlatDataFromZoopla(
        activeUrl.tabId,
        activeUrl.contents,
        (title, url, price) => {
          setActiveFlatData({
            price,
            title,
            url,
          });
        }
      );
    } else if (activeUrl.propertyProvider === "rightmove") {
      getFlatDataFromRightmove(
        activeUrl.tabId,
        activeUrl.contents,
        (title, url, price) => {
          console.log("GET FROM RIGHTMOVE", { title, url, price });
          setActiveFlatData({
            price,
            title,
            url,
          });
        }
      );
    }
  }, [activeUrl]);

  return (
    <Wrapper
      doesFlatMeetRequirements={
        checkIfPropertyMeetsRequirements(
          extractNumber(activeFlatData.price),
          activeFlatData.title
        ).location &&
        checkIfPropertyMeetsRequirements(
          extractNumber(activeFlatData.price),
          activeFlatData.title
        ).price
      }
      isFlatDuplicated={isFlatDuplicated}
    >
      <Text type={TextTypes.title}>{activeFlatData.title}</Text>
      <InfoWrapper>
        {/* Location */}
        {checkIfPropertyMeetsRequirements(
          extractNumber(activeFlatData.price),
          activeFlatData.title
        ).location ? (
          <div style={{ display: "flex", alignItems: "center" }}>
            <Image
              style={{ width: "2.3rem", marginRight: "1rem" }}
              src={checkmark}
              alt="checkmark"
            />
            <Text type={TextTypes.paragraph}>
              Meets your{" "}
              <span style={{ fontWeight: "bold" }}>desired location</span>.
            </Text>
          </div>
        ) : (
          <div style={{ display: "flex", alignItems: "center" }}>
            <Image
              style={{ width: "2.3rem", marginRight: "1rem" }}
              src={cross}
              alt="cross"
            />
            <Text type={TextTypes.paragraph}>
              Does not meet your{" "}
              <span style={{ fontWeight: "bold" }}>desired location</span>.
            </Text>
          </div>
        )}
        {/* Price */}
        {checkIfPropertyMeetsRequirements(
          extractNumber(activeFlatData.price),
          activeFlatData.title
        ).price ? (
          <div style={{ display: "flex", alignItems: "center" }}>
            <Image
              style={{ width: "2.3rem", marginRight: "1rem" }}
              src={checkmark}
              alt="checkmark"
            />
            <Text type={TextTypes.paragraph}>
              Under{" "}
              <span style={{ fontWeight: "bold" }}>£{requirements.price}</span>{" "}
              per month.
            </Text>
          </div>
        ) : (
          <div style={{ display: "flex", alignItems: "center" }}>
            <Image
              style={{ width: "2.3rem", marginRight: "1rem" }}
              src={cross}
              alt="cross"
            />
            <Text type={TextTypes.paragraph}>
              Not under{" "}
              <span style={{ fontWeight: "bold" }}>£{requirements.price}</span>{" "}
              per month.
            </Text>
          </div>
        )}
      </InfoWrapper>
      <div style={{ marginTop: "2rem" }}>
        {isFlatDuplicated ? (
          <Button onClick={removeFlatFromList} label="Remove from list" />
        ) : Object.values(
            checkIfPropertyMeetsRequirements(
              extractNumber(activeFlatData.price),
              activeFlatData.title
            )
          ).some((value) => value === false) ? (
          <Button
            onClick={async () => {
              await addFlat(
                activeFlatData.url,
                activeFlatData.price,
                activeFlatData.title
              );
              setIsFlatDuplicated(true);
            }}
            label="Add to the list anyway"
          />
        ) : (
          <Button
            onClick={async () => {
              await addFlat(
                activeFlatData.url,
                activeFlatData.price,
                activeFlatData.title
              );
              setIsFlatDuplicated(true);
            }}
            label="Add to the list"
          />
        )}
      </div>
      <div style={{ marginTop: 30 }}>
        <p>
          Price: <span style={{ opacity: 0.7 }}>{activeFlatData.price}</span>
        </p>
        <p style={{ marginTop: 5 }}>
          Location: <span style={{ opacity: 0.7 }}>{activeFlatData.title}</span>
        </p>
      </div>
    </Wrapper>
  );

  // if (isFlatDuplicated) {
  //   return (
  //     <Wrapper style={{ backgroundColor: "#322848" }}>
  //       <p>The flat you’re viewing has already been added to the list</p>
  //       <div
  //         style={{ marginTop: 30, display: "flex", flexDirection: "column" }}
  //       ></div>
  //     </Wrapper>
  //   );
  // } else {
  //   return (
  //     <Wrapper>
  //       <p>The flat you are viewing has not been added to the list yet.</p>
  //       <div style={{ marginTop: 30 }}>
  //         <SaveDataButton onClickAction={addFlat} />
  //       </div>
  //     </Wrapper>
  //   );
  // }
};

export default FlatView;
