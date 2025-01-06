import { create } from 'zustand';

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
    }
}));