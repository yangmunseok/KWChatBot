import React from "react";
import MarkDown from "react-markdown";

const Answer = ({ answer }) => {
  return (
    <div className="flex items-start gap-3">
      <div className="w-8 h-8 rounded-full bg-custom/10 flex items-center justify-center">
        <i className="fas fa-robot text-custom"></i>
      </div>
      <div className="bg-gray-100 rounded-lg p-3 max-w-[80%]">
        <MarkDown>{answer}</MarkDown>
      </div>
    </div>
  );
};

export default Answer;
