import React from "react";

interface LoadMoreProps {
  index: number;
  onSelect(): void;
}

const LoadMore: React.FC<LoadMoreProps> = ({ onSelect, index }) => {
  return (
    <div className="h-48 min-h-48 flex items-center justify-center bg-white text-white font-mono font-semibold rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 bg-gradient-to-b from-[#00B4DB] to-[#0083B0]">
      <div className="h-48 flex flex-col items-center justify-center space-y-4">
        <p className="px-8 text-sm">
          Refine your query above or show more places like these.
        </p>
        <button
          onClick={onSelect}
          className="bg-transparent hover:bg-white text-white hover:text-gray-400 py-2 px-4 border border-white hover:border-transparent rounded"
        >
          Show More Places
        </button>
      </div>
    </div>
  );
};

export default LoadMore;
