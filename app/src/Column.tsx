import { Droppable } from "react-beautiful-dnd";
import { Place } from "./App";
import Loader from "./loader/Loader";
import Card from "./places/Card";
import Description from "./places/Description";
import LoadMore from "./places/LoadMore";

interface ColumnProps {
  col: {
    id: string;
    title: string;
    list: Place[];
  };
  loading?: boolean;
  description?: string;
  onGetMore?(): void;
}

const Column: React.FC<ColumnProps> = ({
  col: { id, title, list },
  loading = false,
  description,
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
              {description && <Description text={description} index={-1} />}
              {list.map((place, index) => (
                <Card
                  key={place.id}
                  place={place}
                  index={index}
                  onSelect={(id) => undefined}
                />
              ))}
              {onGetMore && (
                <LoadMore index={list.length + 1} onSelect={onGetMore} />
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
