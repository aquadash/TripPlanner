import React from "react";

interface DescriptionProps {
  index: number;
  text: string;
}

const Description: React.FC<DescriptionProps> = ({ index, text }) => {
  return (
    <div className="h-fit py-8 flex items-center justify-center bg-white text-white font-mono font-semibold rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 bg-gradient-to-b from-[#00B4DB] to-[#0083B0]">
      <div className="row-auto items-center space-y-4">
        <p className="px-8 text-sm">
          {text || "You might be interested in..."}
        </p>
      </div>
    </div>
  );
};

export default Description;
