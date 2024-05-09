import React, { createContext, useState, useContext } from "react";
import {
  _addFlat,
  _createGroup,
  _deleteFlat,
  _getGroupShareCode,
  _getUserGroup,
  _updateGroup,
} from "../utils/resources";
import { extractNumberFromString } from "../utils/util";
import { AxiosError, AxiosRequestHeaders } from "axios";

interface AppContextType {
  activeUrl: any;
  setActiveUrl: any;
  requirements: any;
  setRequirements: any;
  updateRequirements: any;
  flats: Flat[]; // Assuming flats is an array of strings, replace with your actual data type
  setFlats: React.Dispatch<React.SetStateAction<Flat[]>>;
  removeFlat: any; // Define the removeFlat function
  checkIfPropertyMeetsRequirements: (
    price: number,
    location: string
  ) => { location: boolean; price: boolean };
  authenticateUser: any;
  userAuthToken: any;
  setUserAuthToken: any;
  isGroupLoading: boolean;
  userHasGroup: any;
  setUserHasGroup: any;
  getGroup: any;
  getGroupShareCode: any;
  participants: any;
  setParticipants: any;
  createGroup: any;
  addFlat: any;
  appHasError: boolean | string;
  setAppHasError: any;
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
  addedBy?: string;
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

  const [appHasError, setAppHasError] = useState<boolean | string>(false);

  const [userAuthToken, setUserAuthToken] = useState<string | null>(null);
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
        localStorage.removeItem("flatini-auth");
        const authDetails = await chrome.scripting.executeScript({
          target: { tabId: tabs[0].id as number },
          func: () => {
            return localStorage.getItem("flatini-auth-token");
          },
        });
        if ((authDetails as any)[0].result !== "undefined") {
          localStorage.setItem("flatini-auth", (authDetails as any)[0].result);
          setUserAuthToken((authDetails as any)[0].result);
        } else {
          localStorage.removeItem("flatini-auth");
          setUserAuthToken(null);
        }
      }
      getAuthenticationDetails();
    });
  };

  const getGroup = async () => {
    //const token = localStorage.getItem("flatini-auth") as string;
    console.log("usera", userAuthToken);
    if (userAuthToken) {
      try {
        const group = await _getUserGroup(userAuthToken as string);

        if (group) {
          console.log("read group", group);
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
        console.log("err from app provider", err);
        if ((err as AxiosRequestHeaders)?.response?.status === 404) {
          setUserHasGroup(false);
        }

        if ((err as AxiosRequestHeaders)?.response?.status === 401) {
          setAppHasError(
            "Session expired. Please sign back in through flatini.formulathoughts.com and reload the extension"
          );
          localStorage.removeItem("flatini-auth");
          return;
        }

        if ((err as AxiosError)?.code === "ECONNABORTED") {
          setAppHasError(`ECONNABORTED - ${(err as AxiosError).message}`);
          localStorage.removeItem("flatini-auth");
          return;
        }
        setIsGroupLoading(false);
      }
    }
  };

  const updateRequirements = async (
    newPriceLimit: number = requirements.price,
    newLocations: string[] = requirements.locations
  ) => {
    try {
      await _updateGroup(
        userAuthToken as string,
        groupId as string,
        newPriceLimit,
        newLocations
      );
      setRequirements({
        price: newPriceLimit ?? requirements.price,
        locations: newLocations ?? requirements.locations,
        participants: requirements.participants,
      });
    } catch (err) {}
  };

  const createGroup = async () => {
    try {
      const data = await _createGroup(userAuthToken as string);

      if (data && data.group) {
        console.log("data", data);

        setUserHasGroup(true);
        setGroupId(data.group.id);

        // Sets group dependencies
        setFlats(data.group.flats);
        setParticipants(data.group.participants);
        setRequirements({
          price: data.group.priceLimit,
          locations: data.group.locations,
          participants: data.group.participants,
        });
        setIsGroupLoading(false);
        return;
      }

      return data;
    } catch (err) {
      console.log(err);
    }
  };

  const getGroupShareCode = async () =>
    (await _getGroupShareCode(userAuthToken as string, groupId as string)).code;

  /**
   * Flats
   */

  const addFlat = async (url: string, price: string, title: string) => {
    await _addFlat(
      userAuthToken as string,
      groupId as string,
      url,
      extractNumberFromString(price),
      title
    );

    getGroup();
  };

  const removeFlat = async (flatUrl: string) => {
    const findFlat = flats.find((flat) => flat.url === flatUrl);
    if (findFlat) {
      await _deleteFlat(
        userAuthToken as string,
        groupId as string,
        findFlat?.id as string
      );
      getGroup();
    }
  };

  const checkIfPropertyMeetsRequirements = (
    price: number,
    location: string
  ) => {
    console.log("check", price, location);
    console.log(
      "check",
      includesAnySubstring(requirements.locations, location)
    );
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
        updateRequirements,
        checkIfPropertyMeetsRequirements,
        removeFlat,
        // Auth
        authenticateUser,
        userAuthToken,
        setUserAuthToken,
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
        appHasError,
        setAppHasError,
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
