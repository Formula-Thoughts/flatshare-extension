import "./App.css";

import {
  Route,
  BrowserRouter as Router,
  Routes,
  useLocation,
} from "react-router-dom";

import { AuthUser, getCurrentUser, signInWithRedirect } from "aws-amplify/auth";
import { useEffect, useState } from "react";
import Invite from "./views/Invite";
import Homepage from "./views/Homepage";

export default function App() {
  const [user, setUser] = useState<AuthUser | null>(null);

  const getUser = async (): Promise<void> => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.log("Not signed in");
    }
  };

  useEffect(() => {
    getUser();
  });

  if (!user) {
    return (
      <Routes>
        <Route path="/*" element={<Homepage user={user} />} />
      </Routes>
    );
  }

  return (
    <Routes>
      <Route path="/" element={<Homepage user={user} />} />
      <Route path="/invite" element={<Invite user={user} />} />
      <Route path="/signout" element={<p>sign out</p>} />
    </Routes>
  );
}
