import { create } from 'zustand';
import JSEncrypt from 'jsencrypt';
import { redirect } from 'react-router-dom';

export const usePromptStore = create((set) => ({
    prompts:[],
    setPrompts: (prompts) => set({prompts}),
    createPrompt: async(newPrompt) => {
        const res = await fetch("/api/prompts", {method:"POST", headers: {"Content-type":"application/json",}, body:JSON.stringify(newPrompt)});
        const data = await res.json();
        if(!data.success)
            return { success:false, message:data.message };
        set((state) => ({prompts:[...state.prompts,data.data]}));
        return { success:true, message:data.data };
    },
    fetchPrompts: async() => {
        const res = await fetch("/api/prompts")
        const data = await res.json();
        set({prompts: data.data});
    }
}));
