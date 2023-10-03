import React, { createContext, useState, useContext } from "react";
import { _getGroupById } from "../utils/resources";
import { getGroupCode } from "../utils/storage";

interface FlatContextType {
  flats: Flat[]; // Assuming flats is an array of strings, replace with your actual data type
  setFlats: React.Dispatch<React.SetStateAction<Flat[]>>;
  removeFlat: (id: string) => void; // Define the removeFlat function
  initFlatsFromApi: () => Promise<void>;
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

  const initFlatsFromApi = async () => {
    const data = await _getGroupById((await getGroupCode()) as string);
    console.log("data", data);
    setFlats(data?.flats || []);
  };

  const removeFlat = (url: string) => {
    setFlats((prevFlats) => prevFlats.filter((flat) => flat.url !== url));
  };

  return (
    <FlatContext.Provider
      value={{ flats, setFlats, removeFlat, initFlatsFromApi }}
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
