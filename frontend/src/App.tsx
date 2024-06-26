import { Route, Routes, useLocation, useNavigate } from "react-router-dom";

import { AuthUser, getCurrentUser } from "aws-amplify/auth";
import { useEffect, useState } from "react";
import Invite from "./views/Invite";
import Homepage from "./views/Homepage";
import MainLayout from "./views/MainLayout";
import { Hub } from "aws-amplify/utils";

import { fetchAuthSession } from "aws-amplify/auth";

export default function App() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const location = useLocation();
  const navigate = useNavigate();

  const searchParams = new URLSearchParams(location.search);
  const codeFromParam = searchParams.get("groupCode");
  const [inviteCode, setInviteCode] = useState(codeFromParam || "");

  const getUser = async (): Promise<void> => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.log("Not signed in");
    }
  };

  const getTokens = async () => {
    var cognitoTokens = (await fetchAuthSession()).tokens;
    localStorage.setItem(
      "flatini-auth-token",
      cognitoTokens?.accessToken.toString() as string
    );
    console.log("flatauth", cognitoTokens?.accessToken.toString());
  };

  useEffect(() => {
    const getCustomState = Hub.listen("auth", ({ payload }) => {
      switch (payload.event) {
        case "signInWithRedirect":
          getUser();
          break;
        case "customOAuthState":
          if (payload.data) {
            setInviteCode(payload.data);
            navigate("/invite");
          }
          break;
      }
    });

    getUser();
    getTokens();

    console.log("code", inviteCode);
    return getCustomState;
    // Untested next line
  }, [inviteCode, navigate]);

  if (!user) {
    return (
      <MainLayout>
        <Routes>
          <Route
            path="/*"
            element={<Homepage code={inviteCode} user={user} />}
          />
        </Routes>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<Homepage code={inviteCode} user={user} />} />
        <Route
          path="/invite"
          element={<Invite code={inviteCode} user={user} />}
        />
        <Route path="/signout" element={<p>sign out</p>} />
      </Routes>
    </MainLayout>
  );
}
