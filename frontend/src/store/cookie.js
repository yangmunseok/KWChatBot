import { create } from "zustand";
import JSEncrypt from "jsencrypt";
import { redirect } from "react-router-dom";

export const useCookieStore = create((set) => ({
  cookies: [],
  setCookies: (cookies) => set({ cookies }),
  getCookies: async (user) => {
    const login = JSON.stringify({
      loginId: user.userId,
      loginPwd: user.userPwd,
      storeIdYn: "N",
    });
    const body = JSON.stringify({ id: user.userId, password: user.userPwd });
    console.log(body);

    const encrypt = new JSEncrypt();
    const res = await fetch("http://localhost:5000/api/users", {
      headers: {
        "Content-type": "application/json",
      },
      method: "POST",
      body: body,
    });
    const data = await res.json();

    encrypt.setPublicKey(data.public_key);
    const loginToken = encrypt.encrypt(data.login_data);
    console.log("logindata: ", login);
    console.log("loginToken: ", String(loginToken));
    console.log("python loginToken: ", data.login_token);
  },
}));
