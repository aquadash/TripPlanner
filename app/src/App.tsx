import { useCallback, useState } from "react";
import { DragDropContext, DropResult } from "react-beautiful-dnd";
import "./App.css";
import Column from "./Column";
import Map from "./map/Map";
import Navbar from "./navbar/Navbar";
import SearchBar from "./search/SearchBar";

export interface Place {
  id: string;
  name: string;
  description: string;
  address: string;
  location: {
    lat: number;
    lng: number;
  };
  phone: string;
  imageReference: string;
  wheelchair_accessible_entrance: boolean;
  priciness: number;
  rating: number;
  numRatings: number;
  openNow: boolean;
  status: string;
  website: string;
  types: string[];
  keyword: string;
}

interface ApiResponse {
  description: string;
  places: Place[];
}

function App() {
  // const [places, setPlaces] = useState<Place[]>([]);
  // const [itinerary, setItinerary] = useState<Place[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [description, setDescription] = useState<string>("");

  const [selected, setSelected] = useState<string | null>(null);
  // const [isHovered, setIsHovered] = useState<string>("");
  // const handleHoverMarker = (id: string | undefined) => setIsHovered(id);

  const intialState = localStorage.getItem("itinerary");

  const initialColumns = {
    new: {
      id: "new",
      title: "Tailored for You",
      list: [],
    },
    itinerary: {
      id: "itinerary",
      title: "Your Itinerary",
      list: JSON.parse(intialState) || [],
    },
  };
  const [columns, setColumns] = useState(initialColumns);

  const onDragEnd = ({ source, destination }: DropResult) => {
    // Make sure we have a valid destination
    if (destination === undefined || destination === null) return null;

    // Make sure we're actually moving the item
    if (
      source.droppableId === destination.droppableId &&
      destination.index === source.index
    )
      return null;

    // Set start and end variables
    const start = columns[source.droppableId];
    const end = columns[destination.droppableId];

    // If start is the same as end, we're in the same column
    if (start === end) {
      // Move the item within the list
      // Start by making a new list without the dragged item
      const newList = start.list.filter(
        (_: any, idx: number) => idx !== source.index
      );

      // Then insert the item at the right location
      newList.splice(destination.index, 0, start.list[source.index]);

      // Then create a new copy of the column object
      const newCol = {
        id: start.id,
        title: start.title,
        list: newList,
      };

      // Update the state
      setColumns((state) => ({ ...state, [newCol.id]: newCol }));
      if (newCol.id === "itinerary") {
        console.log("Reordering itinerary");
        localStorage.setItem("itinerary", JSON.stringify(newCol.list));
      }
      return null;
    } else {
      // If start is different from end, we need to update multiple columns
      // Filter the start list like before
      const newStartList = start.list.filter(
        (_: any, idx: number) => idx !== source.index
      );

      // Create a new start column
      const newStartCol = {
        id: start.id,
        title: start.title,
        list: newStartList,
      };

      // Make a new end list array
      const newEndList = end.list;

      // Insert the item into the end list
      newEndList.splice(destination.index, 0, start.list[source.index]);

      // Create a new end column
      const newEndCol = {
        id: end.id,
        title: end.title,
        list: newEndList,
      };

      // Update the state
      setColumns((state) => ({
        ...state,
        [newStartCol.id]: newStartCol,
        [newEndCol.id]: newEndCol,
      }));
      if (newStartCol.id === "itinerary") {
        console.log("Removing from itinerary");
        localStorage.setItem("itinerary", JSON.stringify(newStartCol.list));
      }
      if (newEndCol.id === "itinerary") {
        console.log("Saving to itinerary");
        localStorage.setItem("itinerary", JSON.stringify(newEndCol.list));
      }
      return null;
    }
  };

  const onGetResults = useCallback(
    async (query: any, retry?: number) => {
      setIsLoading(true);
      fetch(
        `https://govhack-tripplanner.azurewebsites.net/api/places?query='${query}'&retry=${retry}`
      )
        .then((response) => response.json())
        .then(async (data: ApiResponse) => {
          setDescription(data.description);
          const deDuplicatedPlaces = data.places.filter(
            (place: Place) =>
              !columns.itinerary.list.some(
                (itineraryPlace: Place) => itineraryPlace.id === place.id
              )
          );
          setColumns((state) => ({
            ...state,
            new: {
              id: state.new.id,
              title: state.new.title,
              list: deDuplicatedPlaces,
            },
          }));
        })
        .catch((error) => console.log(error))
        .finally(() => setIsLoading(false));
    },
    [columns.itinerary.list]
  );

  const handleGetMore = () => {
    console.log("user wants to get more");

    // onGetResults(query, 1);
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <Navbar />
      <SearchBar sendQuery={onGetResults} />
      <div className="App grid grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <h2 className="font-mono font-semibold">{columns.new.title}</h2>
          <Column
            loading={isLoading}
            col={columns.new}
            description={
              description !== "" && columns.new.list.length > 0
                ? description
                : undefined
            }
            onGetMore={handleGetMore}
          />
        </div>

        <div>
          <h2 className="font-mono font-semibold">{columns.itinerary.title}</h2>
          <Column col={columns.itinerary} />
        </div>

        <div className="md:block hidden">
          <h2 className="font-mono font-semibold mb-2">Where is it?</h2>
          <Map
            places={columns.itinerary.list}
            goto={selected}
            selected={selected}
            onMarkerClick={(id: string | null) => setSelected(id)}
          />
        </div>
      </div>
    </DragDropContext>
  );
}

export default App;
