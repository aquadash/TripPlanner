import { GridLoader } from "react-spinners";

const Loader = () => {
  return (
    <div
      className="
      h-[70vh]
      flex 
      flex-col 
      justify-center 
      items-center 
    "
    >
      <GridLoader size={20} color="black" aria-label="Loading Spinner" />
      <span className="mt-4 font-mono">Creating Itinerary</span>
    </div>
  );
};

export default Loader;
