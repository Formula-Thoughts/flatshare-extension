import React, { createContext, useState, useContext } from "react";

interface FlatContextType {
  flats: Flat[]; // Assuming flats is an array of strings, replace with your actual data type
  setFlats: React.Dispatch<React.SetStateAction<Flat[]>>;
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

  return (
    <FlatContext.Provider value={{ flats, setFlats }}>
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
