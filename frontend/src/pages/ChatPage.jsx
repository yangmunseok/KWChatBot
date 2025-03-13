import { React, useEffect, useState } from "react";
import { usePromptStore } from "@/store/prompt";
import Question from "@/components/ui/Question";
import Answer from "@/components/ui/Answer";
import { useQuery } from "@tanstack/react-query";

const ChatPage = () => {
  const [newPrompt, setNewPrompt] = useState({ question: "" });
  const { data: apiKey } = useQuery({
    queryKey: ["apiKey"],
  });
  const { prompts, createPrompt, fetchPrompts } = usePromptStore();
  const HandleAddPrompt = async () => {
    const { success, message } = await createPrompt(newPrompt, apiKey);
    setNewPrompt({ question: "" });
  };
  useEffect(() => {
    fetchPrompts();
  }, [fetchPrompts]);
  return (
    <main className="flex-grow pt-20 pb-16 max-w-8xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex gap-6">
        <aside className="w-64 hidden lg:block">
          <div className="bg-white rounded-lg shadow-sm p-4">
            <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 !rounded-button">
                Tell me a joke
              </button>
              <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 !rounded-button">
                Weather forecast
              </button>
              <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 !rounded-button">
                Set a reminder
              </button>
              <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 !rounded-button">
                Play music
              </button>
            </div>
          </div>
        </aside>

        <div className="flex-1">
          <div className="bg-white rounded-lg shadow-sm flex flex-col">
            <div className="flex-1 p-4 space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-custom/10 flex items-center justify-center">
                  <i className="fas fa-robot text-custom"></i>
                </div>
                <div className="bg-gray-100 rounded-lg p-3 max-w-[80%]">
                  <p className="text-gray-800">
                    Hello! How can I assist you today?
                  </p>
                </div>
              </div>
              {prompts.map((prompt) => (
                <div key={prompt._id} className="space-y-4">
                  <Question question={prompt.question} />
                  <Answer answer={prompt.final_response} />
                </div>
              ))}
            </div>
            <div className="border-t p-4">
              <div className="flex gap-3">
                <button className="p-2 text-gray-500 hover:text-custom">
                  <i className="fas fa-microphone"></i>
                </button>
                <button className="p-2 text-gray-500 hover:text-custom">
                  <i className="fas fa-paperclip"></i>
                </button>
                <input
                  type="text"
                  placeholder="Type your message..."
                  className="flex-1 border-0 focus:ring-0 bg-gray-100 rounded-lg text-black"
                  value={newPrompt.question}
                  onChange={(e) =>
                    setNewPrompt({ ...newPrompt, question: e.target.value })
                  }
                />
                <button
                  className="bg-custom text-white px-4 py-2 !rounded-button hover:bg-custom/90"
                  onClick={HandleAddPrompt}
                >
                  <i className="fas fa-paper-plane"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default ChatPage;
