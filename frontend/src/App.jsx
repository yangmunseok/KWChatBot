import { Box, Button } from "@chakra-ui/react";
import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/ui/Navbar";
import ChatPage from "./pages/ChatPage";
import Footer from "./components/ui/Footer";
import LoginPage from "./pages/LoginPage";
import { useQuery } from "@tanstack/react-query";
import SignupPage from "./pages/SignupPage";
import SettingPage from "./pages/SettingPage";
import MainPage from "./pages/MainPage";
import FAQPage from "./pages/FAQPage";

function App() {
  const {
    data: authUser,
    isPending,
    isError,
    refetch,
  } = useQuery({
    queryKey: ["authUser"],
    queryFn: async () => {
      try {
        const res = await fetch("/api/auth/getme");
        const data = await res.json();

        //for quick logout
        if (data?.error || data?.detail?.error) {
          return null;
        }

        if (!res.ok) {
          throw new Error(
            data.detail.error || data.error || "something went wrong!"
          );
        }

        return data;
      } catch (error) {
        throw new Error(error);
      }
    },
  });

  if (isPending) {
    return (
      <div class="h-screen w-full py-20 relative flex md:flex-row flex-col gap-10 justify-center items-center bg-white">
        <div class="border-gray-300 h-20 w-20 animate-spin rounded-full border-8 border-t-blue-600" />
      </div>
    );
  }

  return (
    <div className="font-[Inter] bg-gray-50 flex flex-col min-h-screen">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate replace to="/main" />} />
        <Route path="/main" element={<MainPage />} />
        <Route path="/faq" element={<FAQPage />} />
        <Route
          path="/chat"
          element={authUser ? <ChatPage /> : <Navigate replace to="/login" />}
        />
        <Route
          path="/login"
          element={!authUser ? <LoginPage /> : <Navigate replace to="/main" />}
        />
        <Route
          path="/signup"
          element={!authUser ? <SignupPage /> : <Navigate replace to="/main" />}
        />
        <Route
          path="/setting"
          element={
            authUser ? <SettingPage /> : <Navigate replace to="/login" />
          }
        />
      </Routes>
      <Footer />
    </div>
  );
}
export default App;
