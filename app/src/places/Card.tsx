import React from "react";
import { Place } from "../App";
import { Draggable } from "react-beautiful-dnd";
import { FaWheelchair } from "react-icons/fa";
interface CardProps {
  place: Place;
  index: number;
  onSelect(id: string): void;
}

const Card: React.FC<CardProps> = ({ place, onSelect, index }) => {
  return (
    <Draggable draggableId={place.id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          onClick={() => onSelect(place.id)}
          className="hover:shadow-md"
          // className="h-48 cursor-pointer hover:shadow-lg flex flex-col items-end bg-white rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 scale-95 hover:scale-100 ease-in-out duration-100"
        >
          {place.keyword && (
            <div className="absolute m-1 align-top flex">
              <span className="bg-green-100 font-mono text-green-800 text-sm font-semibold px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300">
                {place.keyword || "For You"}
              </span>
            </div>
          )}
          <div
            style={{
              backgroundImage: `url(${place.imageReference})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
            className="h-48 flex flex-col items-end bg-white rounded-lg shadow md:flex-row md:max-w-xl"
          >
            <div className="bg-slate-200 text-[#0393A1] text-left font-mono font-thin p-1 rounded-tr-md rounded-bl-md flex-col">
              <span className="font-semibold">{place.name}</span>

              <span className="text-sm">
                <div className="flex items-center">
                  <svg
                    className="h-4 text-[#0393A1]-300 mr-1"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 22 20"
                  >
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
                  </svg>
                  <p className="ml-1 text-sm font-semibold">{place.rating}</p>
                  <p className="text-sm ml-2">({place.numRatings} reviews)</p>
                  {place.wheelchair_accessible_entrance && (
                    <p className="text-sm ml-2 flex items-center gap-1">
                      <FaWheelchair className="font-semibold" /> Friendly
                    </p>
                  )}
                  {/* <span className="ml-2 bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded border-green-400">
                    Open
                  </span> */}
                </div>
              </span>
            </div>
          </div>
        </div>
      )}
    </Draggable>
  );
};

export default Card;
