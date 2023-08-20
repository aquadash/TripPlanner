import { Droppable } from "react-beautiful-dnd";
import { Place } from "./App";
import Card from "./places/Card";
import LoadMore from "./places/LoadMore";
import Loader from "./loader/Loader";

interface ColumnProps {
  col: {
    id: string;
    title: string;
    list: Place[];
  };
  loading?: boolean;
  onGetMore?(): void;
}

const Column: React.FC<ColumnProps> = ({
  col: { id, title, list },
  loading = false,
  onGetMore,
}) => {
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
          {loading ? (
            <Loader />
          ) : (
            <>
              {list.map((place, index) => (
                <Card
                  key={place.id}
                  place={place}
                  index={index}
                  onSelect={(id) => undefined}
                />
              ))}
              {onGetMore && (
                <LoadMore index={list.length} onSelect={onGetMore} />
              )}
            </>
          )}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );
};

export default Column;
