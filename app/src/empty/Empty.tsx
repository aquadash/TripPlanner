const Empty = () => {
  return (
    <div className="container mx-auto my-8 space-y-10">
      <div className="flex flex-col justify-center py-3 items-center">
        <div className="flex justify-center items-center">
          <img className="w-32 h-32" src="travel-bag.png" alt="empty states" />
        </div>
        <h1 className="text-gray-700 font-medium text-2xl text-center mb-3 mt-4">
          The World Awaits You
        </h1>
        <p className="text-gray-500 text-center mb-6">
          Tell us where you are going, your accessibility requirements, and the
          kind of stuff you're into.
        </p>
      </div>
    </div>
  );
};

export default Empty;
