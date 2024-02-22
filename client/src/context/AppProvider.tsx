import React, { createContext, useState, useContext } from "react";
import { _getGroupById } from "../utils/resources";

interface FlatContextType {
  activeUrl: any;
  setActiveUrl: any;
  requirements: any;
  setRequirements: any;
  flats: Flat[]; // Assuming flats is an array of strings, replace with your actual data type
  setFlats: React.Dispatch<React.SetStateAction<Flat[]>>;
  removeFlat: (id: string) => void; // Define the removeFlat function
  initFlatsFromApi: () => Promise<void>;
  checkIfPropertyMeetsRequirements: (
    price: number,
    location: string
  ) => { location: boolean; price: boolean };
}

export type Flat = {
  id: string;
  title: string;
  url: string;
  price: string;
};

export type Props = {
  children: JSX.Element[] | JSX.Element;
};

const FlatContext = createContext<FlatContextType | undefined>(undefined);

const FlatProvider = (props: Props) => {
  const [activeUrl, setActiveUrl] = useState<
    | {
        tabId: number;
        contents: string;
      }
    | {}
  >({});
  const [flats, setFlats] = useState<Flat[]>([]);
  const [requirements, setRequirements] = useState<{
    price: number;
    location: string[];
  }>({
    price: 3000,
    location: ["W1H", "E1W"],
  });

  const initFlatsFromApi = async () => {
    setFlats([]);
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
      location: includesAnySubstring(requirements.location, location),
      price: requirements.price >= price,
    };
  };

  return (
    <FlatContext.Provider
      value={{
        activeUrl,
        setActiveUrl,
        flats,
        setFlats,
        requirements,
        setRequirements,
        checkIfPropertyMeetsRequirements,
        removeFlat,
        initFlatsFromApi,
      }}
    >
      {props.children}
    </FlatContext.Provider>
  );
};

export const useFlats = () => {
  const context = useContext(FlatContext);
  if (!context) {
    throw new Error("useFlats must be used within a FlatProvider");
  }
  return context;
};

export default FlatProvider;
