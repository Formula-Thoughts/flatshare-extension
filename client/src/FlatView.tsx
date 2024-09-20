import { createContext, useEffect, useState } from "react";
import styled from "styled-components";
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
import { Link, useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import Loading from "./views/Loading";
import { _getPropertyRedFlags } from "./utils/resources";

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
  gap: 2rem;
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
  gap: 1rem;
  display: flex;
  flex-direction: column;
`;

const RedFlagsBanner = styled.div`
  cursor: pointer;
  position: relative;
  border: 1px solid #ffffff5c;
  background: white;
  color: black;
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  gap: 1rem;
`;

const FlatView = () => {
  const navigate = useNavigate();
  const {
    flats,
    addFlat,
    activeUrl,
    checkIfPropertyMeetsRequirements,
    requirements,
    removeFlat,
    setAppHasError,
    userAuthToken,
    activeFlatData,
    setActiveFlatData,
  } = useProvider();
  const [isFlatDuplicated, setIsFlatDuplicated] = useState(false);
  const [loadingFlatData, setLoadingFlatData] = useState(true);

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

  const getDataFromActiveTab = () => {
    checkFlatIsDuplicated();
    console.log(
      "5 [getDataFromActiveFlat - FlatView.tsx] -> Gets data from active flat"
    );

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length > 0) {
        const activeTab = tabs[0];

        if (activeUrl.propertyProvider === "openrent") {
          getFlatDataFromOpenRent(
            activeUrl.tabId,
            activeUrl.contents,
            (title, url, price) => {
              setActiveFlatData({
                ...activeFlatData,
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
                ...activeFlatData,
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
                ...activeFlatData,
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
              setActiveFlatData({
                ...activeFlatData,
                price,
                title,
                url,
              });
            }
          );
        }
      }
    });
  };

  const removeFlatFromList = () => {
    console.log("activeurl, contents", activeUrl.contents);
    removeFlat(activeUrl.contents);
    setIsFlatDuplicated(false);
  };

  const getRedFlags = async () => {
    const redFlags = await _getPropertyRedFlags(
      userAuthToken as string,
      activeFlatData?.url
    );
    setActiveFlatData({ ...activeFlatData, redFlags: redFlags.redFlags });
    console.log(
      "7 [getRedFlags - FlatView.tsx] -> Gets red flags but doesn't trigger activeFlatData to update",
      activeFlatData
    );
  };

  useEffect(() => {
    if (activeUrl?.contents) {
      setLoadingFlatData(true);
      console.log(
        "4 [useEffect - FlatView.tsx] -> Flatview loads, and watches for changes on activeUrl.contents"
      );
      getDataFromActiveTab();
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeUrl?.contents]);

  useEffect(() => {
    if (activeFlatData?.url) {
      console.log(
        "6 [useEffect 2 - FlatView.tsx] -> Triggers when activeFlatData url changes",
        activeFlatData
      );
      getRedFlags();
    }
  }, [activeFlatData?.url]);

  useEffect(() => {
    if (activeFlatData?.redFlags) {
      console.log(
        "8 [useEffect 3 - FlatView.tsx] -> When red flags have been set, it sets flat view loading state to false",
        activeFlatData
      );
      setLoadingFlatData(false);
    }
  }, [activeFlatData?.redFlags]);

  if (loadingFlatData) {
    return <Loading />;
  }

  if (
    !activeFlatData?.price ||
    !activeFlatData?.title ||
    !activeFlatData?.url
  ) {
    setAppHasError(
      "Sorry. This property cannot be added to your list, would you mind reloading the extension? :)"
    );
  }
  if (activeFlatData) {
    return (
      <Wrapper
        doesFlatMeetRequirements={
          checkIfPropertyMeetsRequirements(
            extractNumber(activeFlatData?.price),
            activeFlatData?.title
          ).location &&
          checkIfPropertyMeetsRequirements(
            extractNumber(activeFlatData?.price),
            activeFlatData?.title
          ).price
        }
        isFlatDuplicated={isFlatDuplicated}
      >
        <Link to="/">
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "0.5rem",
              cursor: "pointer",
              opacity: 0.7,
            }}
          >
            <FaArrowLeft />
            <Text type={TextTypes.paragraph}>Back to my list</Text>
          </div>
        </Link>
        <Text type={TextTypes.title}>{activeFlatData?.title}</Text>
        <InfoWrapper>
          {/* Location */}
          {checkIfPropertyMeetsRequirements(
            extractNumber(activeFlatData?.price),
            activeFlatData?.title
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
          {requirements.price ? (
            checkIfPropertyMeetsRequirements(
              extractNumber(activeFlatData?.price),
              activeFlatData?.title
            ).price ? (
              <div style={{ display: "flex", alignItems: "center" }}>
                <Image
                  style={{ width: "2.3rem", marginRight: "1rem" }}
                  src={checkmark}
                  alt="checkmark"
                />
                <Text type={TextTypes.paragraph}>
                  Under{" "}
                  <span style={{ fontWeight: "bold" }}>
                    £{requirements.price}
                  </span>{" "}
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
                  <span style={{ fontWeight: "bold" }}>
                    £{requirements.price}
                  </span>{" "}
                  per month.
                </Text>
              </div>
            )
          ) : null}
        </InfoWrapper>
        <div>
          {isFlatDuplicated ? (
            <Button onClick={removeFlatFromList} label="Remove from list" />
          ) : Object.values(
              checkIfPropertyMeetsRequirements(
                extractNumber(activeFlatData?.price),
                activeFlatData?.title
              )
            ).some((value) => value === false) ? (
            <Button
              onClick={async () => {
                await addFlat(
                  activeFlatData?.url,
                  activeFlatData?.price,
                  activeFlatData?.title
                );
                setIsFlatDuplicated(true);
              }}
              label="Add to the list anyway"
            />
          ) : (
            <Button
              onClick={async () => {
                await addFlat(
                  activeFlatData?.url,
                  activeFlatData?.price,
                  activeFlatData?.title
                );
                setIsFlatDuplicated(true);
              }}
              label="Add to the list"
            />
          )}
        </div>
        <div>
          <p>
            Price: <span style={{ opacity: 0.7 }}>{activeFlatData?.price}</span>
          </p>
          <p style={{ marginTop: 5 }}>
            Location:{" "}
            <span style={{ opacity: 0.7 }}>{activeFlatData?.title}</span>
          </p>
        </div>
        {activeFlatData?.redFlags?.length === 0 ? (
          <Button
            style={{
              width: "100%",
            }}
            onClick={() =>
              navigate("/AddRedFlag", {
                state: {
                  flatName: activeFlatData?.title,
                  flatUrl: activeFlatData?.url,
                },
              })
            }
            label="🚩 Add red flag"
          />
        ) : (
          <RedFlagsBanner onClick={() => navigate("/RedFlags")}>
            <span style={{ fontSize: "2rem" }}>🚩</span>
            <div>
              <Text type={TextTypes.paragraph}>
                Some users have spotted {activeFlatData?.redFlags?.length} red
                flag(s) in this property.
              </Text>
              <Text
                style={{
                  position: "absolute",
                  right: 0,
                  bottom: 0,
                  opacity: 0.5,
                  margin: "0.5rem",
                  fontSize: "1rem",
                }}
                type={TextTypes.paragraph}
              >
                See ({activeFlatData?.redFlags?.length})
              </Text>
            </div>
          </RedFlagsBanner>
        )}
      </Wrapper>
    );
  }
  return <div />;
};

export default FlatView;
