import { InfoWindowF } from "@react-google-maps/api";
import React, { useEffect, useState } from "react";
import { MAP_SETTINGS } from "./Polyline";
import { Place } from "../App";

interface DistanceInfoProps {
  from: Place;
  to: Place;
}

const toDistance = (distance: number) => {
  if (distance >= 1000) {
    return Math.round(distance / 1000.0) + " km";
  } else {
    return distance.toFixed(1) + " m";
  }
};

const DistanceInfo: React.FC<DistanceInfoProps> = ({ from, to }) => {
  const [lineCenter, setLineCenter] = useState<google.maps.LatLng>();

  useEffect(() => {
    const calculateLineCenter = async () => {
      if (typeof window !== "undefined") {
        const center = window.google.maps.geometry.spherical.interpolate(
          new window.google.maps.LatLng(
            Number(from.location.lat),
            Number(from.location.lng)
          ),
          new window.google.maps.LatLng(
            Number(to.location.lat),
            Number(to.location.lng)
          ),
          0.5
        );
        setLineCenter(center);
      }
    };

    calculateLineCenter();
  }, [from, to]);

  return (
    lineCenter && (
      <InfoWindowF
        position={lineCenter}
        zIndex={98}
        options={{
          pixelOffset: new google.maps.Size(
            MAP_SETTINGS.PIXEL_OFFSET.X,
            MAP_SETTINGS.PIXEL_OFFSET.Y
          ),
        }}
      >
        <div
          style={{ backgroundColor: false ? "#fada5e" : "#247291" }}
          className={`rounded-md p-2 font-medium items-center inline-flex ${
            false ? "text-black" : "text-white"
          }`}
        >
          {toDistance(parseFloat("123.45"))}
        </div>
      </InfoWindowF>
    )
  );
};

export default DistanceInfo;
