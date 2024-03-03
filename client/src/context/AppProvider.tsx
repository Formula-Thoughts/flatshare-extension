import React, { createContext, useState, useContext } from "react";
import {
  _createGroup,
  _getGroupById,
  _getGroupShareCode,
  _getUserGroup,
} from "../utils/resources";
import { group } from "console";
import { getObjectByKeyPart } from "../utils/util";
import { AxiosRequestHeaders } from "axios";

interface AppContextType {
  activeUrl: any;
  setActiveUrl: any;
  requirements: any;
  setRequirements: any;
  flats: Flat[]; // Assuming flats is an array of strings, replace with your actual data type
  setFlats: React.Dispatch<React.SetStateAction<Flat[]>>;
  removeFlat: (id: string) => void; // Define the removeFlat function
  checkIfPropertyMeetsRequirements: (
    price: number,
    location: string
  ) => { location: boolean; price: boolean };
  authenticateUser: any;
  getAuthenticatedUser: any;
  isGroupLoading: boolean;
  userHasGroup: any;
  setUserHasGroup: any;
  getGroup: any;
  getGroupShareCode: any;
  participants: any;
  setParticipants: any;
  createGroup: any;
}

export type Group = {
  flats: Flat[];
  participants: [];
  priceLimit: 1000;
  location: "Hammersmith, London";
};

export type Flat = {
  id: string;
  title: string;
  url: string;
  price: string;
};

export type Props = {
  children: JSX.Element[] | JSX.Element;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

const FlatProvider = (props: Props) => {
  const [activeUrl, setActiveUrl] = useState<
    | {
        tabId: number;
        contents: string;
      }
    | {}
  >({});
  const [isGroupLoading, setIsGroupLoading] = useState<boolean>(true);
  const [userHasGroup, setUserHasGroup] = useState<boolean>(false);
  const [flats, setFlats] = useState<Flat[]>([]);
  const [participants, setParticipants] = useState<string[]>([]);
  const [requirements, setRequirements] = useState<{
    price: number;
    location: string[];
  }>({
    price: 3000,
    location: ["W1H", "E1W"],
  });

  /**
   * Authentication
   */

  // Gets local storage from main active tab and saves token in extension's local storage
  const authenticateUser = () => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      async function getAuthenticationDetails() {
        const authDetails = await chrome.scripting.executeScript({
          target: { tabId: tabs[0].id as number },
          func: () => {
            return JSON.stringify(localStorage);
          },
        });
        if ((authDetails as any)[0].result !== "{}") {
          localStorage.setItem(
            "flatini-auth",
            JSON.stringify((authDetails as any)[0].result)
          );
        } else {
          localStorage.removeItem("flatini-auth");
        }
      }
      getAuthenticationDetails();
    });
  };

  // Gets authenticated user
  const getAuthenticatedUser = () =>
    (localStorage.getItem("flatini-auth") as string) || null;

  const getGroup = async () => {
    // Get group from the API
    // const group = {
    //   flats: [],
    //   participants: ["Xav", "Dom"],
    //   priceLimit: 1000,
    //   location: "Hammersmith, London",
    // };

    try {
      const group = await _getUserGroup(
        getObjectByKeyPart(
          "accessToken",
          JSON.parse(JSON.parse(getAuthenticatedUser() as string))
        )
      );

      if (group) {
        // Sets state dependencies
        setFlats(group.flats);
        setParticipants(group.participants);
        setUserHasGroup(true);
        setRequirements({
          price: group.priceLimit,
          location: [group.location],
        });
        setIsGroupLoading(false);
        return;
      }
    } catch (err) {
      if ((err as AxiosRequestHeaders)?.response?.status === 404) {
        setUserHasGroup(false);
      }
      setIsGroupLoading(false);
    }
  };

  const createGroup = async () => {
    const data = await _createGroup(
      getObjectByKeyPart(
        "accessToken",
        JSON.parse(JSON.parse(getAuthenticatedUser() as string))
      )
    );

    console.log(data);

    return data;
  };

  const getGroupShareCode = async () => {
    // should be getting group id from state
    // return await _getGroupShareCode(group.id);
    return "code test";
  };

  /**
   * Flats
   */

  const removeFlat = (url: string) => {
    setFlats((prevFlats) => prevFlats.filter((flat) => flat.url !== url));
  };

  const checkIfPropertyMeetsRequirements = (
    price: number,
    location: string
  ) => {
    function includesAnySubstring(arr: string[], str: string): boolean {
      return arr.some((substring) => str.includes(substring));
    }
    return {
      location: includesAnySubstring(requirements.location, location),
      price: requirements.price >= price,
    };
  };

  return (
    <AppContext.Provider
      value={{
        activeUrl,
        setActiveUrl,
        flats,
        setFlats,
        requirements,
        setRequirements,
        checkIfPropertyMeetsRequirements,
        removeFlat,
        // Auth
        authenticateUser,
        getAuthenticatedUser,
        // Groups
        isGroupLoading,
        userHasGroup,
        setUserHasGroup,
        getGroup,
        getGroupShareCode,
        participants,
        setParticipants,
        createGroup,
      }}
    >
      {props.children}
    </AppContext.Provider>
  );
};

export const useProvider = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useProvider must be used within a FlatProvider");
  }
  return context;
};

export default FlatProvider;
