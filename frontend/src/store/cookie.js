import { create } from 'zustand';
import JSEncrypt from 'jsencrypt';
import { redirect } from 'react-router-dom';

export const useCookieStore = create((set) => ({
    cookies:[],
    setCookies: (cookies) => set({cookies}),
    getCookies: async(user) => {
        const login = JSON.stringify({loginId: user.userId, loginPwd: user.userPwd, storeIdYn: 'N'});
        const encrypt = new JSEncrypt();
        const res1 = await fetch("https://klas.kw.ac.kr/usr/cmn/login/LoginSecurity.do");
        const data1 = await res1.json();
        encrypt.setPublicKey(data1.publicKey);
        const loginToken = encrypt.encrypt(login);
        const res = await fetch("https://klas.kw.ac.kr/usr/cmn/login/LoginConfirm.do", {method:"POST", headers: {"Content-type":"application/json",}, body:JSON.stringify({loginToken:loginToken,redirectUrl:"",redirectTabUrl:""})});
        console.log(res);
    }
}));