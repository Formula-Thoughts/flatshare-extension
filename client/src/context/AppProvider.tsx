import React, { createContext, useState, useContext } from "react";
import {
  _addFlat,
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
  addFlat: any;
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
  // Renders dashboard screens
  const [isGroupLoading, setIsGroupLoading] = useState<boolean>(true);

  // If user doesn't have group, it will show Create Group screen
  const [userHasGroup, setUserHasGroup] = useState<boolean>(false);

  // Group dependencies
  const [groupId, setGroupId] = useState<string | null>(null);
  const [flats, setFlats] = useState<Flat[]>([]);
  const [participants, setParticipants] = useState<string[]>([]);
  const [requirements, setRequirements] = useState<{
    price: number;
    locations: string[];
    participants: string[];
  }>({
    price: 3000,
    locations: ["W1H", "E1W"],
    participants: [],
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

  const getAccessToken = (): string =>
    getObjectByKeyPart(
      "accessToken",
      JSON.parse(JSON.parse(getAuthenticatedUser() as string))
    );

  const getGroup = async () => {
    try {
      const group = await _getUserGroup(getAccessToken());

      if (group) {
        setUserHasGroup(true);
        setGroupId(group?.groups[0].id);

        // Sets group dependencies
        setFlats(group?.groups[0].flats);
        setParticipants(group?.groups[0].participants);
        setRequirements({
          price: group?.groups[0].priceLimit,
          locations: group?.groups[0].locations,
          participants: group?.groups[0].participants,
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
    try {
      const data = await _createGroup(getAccessToken());

      if (data && data.group) {
        // Sets state dependencies
        setFlats(data.group.flats);
        setParticipants(data.group.flats);
        setUserHasGroup(true);
        setRequirements({
          price: data.group.priceLimit,
          locations: data.group.locations,
          participants: data.group.participants,
        });
        setIsGroupLoading(false);
        return;
      }

      console.log(data);

      return data;
    } catch (err) {
      console.log(err);
    }
  };

  const getGroupShareCode = async () =>
    (await _getGroupShareCode(getAccessToken(), groupId as string)).code;

  /**
   * Flats
   */

  const addFlat = async (url: string, price: number, location: string) => {
    return await _addFlat(
      getAccessToken(),
      groupId as string,
      url,
      price,
      location
    );
  };

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
      location: includesAnySubstring(requirements.locations, location),
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
        addFlat,
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
