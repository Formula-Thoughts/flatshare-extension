import React, { createContext, useState, useContext } from "react";

interface FlatContextType {
  flats: Flat[]; // Assuming flats is an array of strings, replace with your actual data type
  setFlats: React.Dispatch<React.SetStateAction<Flat[]>>;
  removeFlat: (id: string) => void; // Define the removeFlat function
  setGroupCode: (code: string) => void;
  getGroupCode: () => Promise<string | undefined>;
}

export type Flat = {
  id: string;
  title: string;
  url: string;
  price: string;
};

export type Props = {
  children: JSX.Element[];
};

const FlatContext = createContext<FlatContextType | undefined>(undefined);

const FlatProvider = (props: Props) => {
  const [flats, setFlats] = useState<Flat[]>([]); // Initialize state here

  const removeFlat = (url: string) => {
    setFlats((prevFlats) => prevFlats.filter((flat) => flat.url !== url));
  };

  const setGroupCode = (code: string) => {
    chrome.storage.local.set({ groupCode: code }, function () {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      }
    });
  };

  const getGroupCode = async () => {
    return new Promise<string | undefined>((resolve) => {
      chrome.storage.local.get("groupCode", function (result) {
        if (chrome.runtime.lastError) {
          console.error(chrome.runtime.lastError);
          resolve(undefined);
        } else {
          const groupCode = result.groupCode;
          resolve(groupCode);
        }
      });
    });
  };

  return (
    <FlatContext.Provider
      value={{ flats, setFlats, removeFlat, setGroupCode, getGroupCode }}
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
