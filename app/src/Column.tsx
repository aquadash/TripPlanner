import { Droppable } from "react-beautiful-dnd";
import { Place } from "./App";
import Card from "./places/Card";

interface ColumnProps {
  col: {
    id: string;
    title: string;
    list: Place[];
  };
}

const Column: React.FC<ColumnProps> = ({ col: { id, title, list } }) => {
  return (
    <Droppable droppableId={id}>
      {(provided) => (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            backgroundColor: "#eee",
            borderRadius: "9px",
            padding: 16,
            flexGrow: 1,
            marginTop: 8,
          }}
          {...provided.droppableProps}
          ref={provided.innerRef}
          className="space-y-2 h-screen overflow-x-hidden"
        >
          <>
            {list.map((place, index) => (
              <Card
                key={place.id}
                place={place}
                index={index}
                onSelect={(id) => undefined}
              />
            ))}
          </>
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );
};

export default Column;
