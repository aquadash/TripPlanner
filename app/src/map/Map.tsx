"use client";

import {
  GoogleMap,
  InfoWindowF,
  MarkerF,
  Polyline,
  useJsApiLoader,
} from "@react-google-maps/api";
import React, { CSSProperties, useCallback, useEffect, useState } from "react";
import { Place } from "../App";
import Loader from "../loader/Loader";
import { MAP_SETTINGS } from "./Polyline";
import silverMapStyle from "./silverStyle.json";
import DistanceInfo from "./DistanceInfo";

const containerStyle: CSSProperties = {
  width: "100%",
  height: "100%",
  borderRadius: "9px",
};

const center = {
  lat: -2.5674,
  lng: 134.9893,
};

interface MapProps {
  style?: CSSProperties;
  goto?: string;
  places: Place[];
  containerStyle?: CSSProperties;
  onMarkerClick: (id: string | null) => void;
  selected: string | null;
}

const Map: React.FC<MapProps> = (props) => {
  const {
    places,
    goto,
    style = containerStyle,
    onMarkerClick,
    selected,
  } = props;

  const { isLoaded } = useJsApiLoader({
    id: "places-map",
    googleMapsApiKey: String(process.env.REACT_APP_GOOGLE_MAPS_API_KEY),
  });

  const [map, setMap] = useState<google.maps.Map | undefined>();

  const onLoad = React.useCallback(function callback(map: google.maps.Map) {
    // if (center) {
    //   map.setCenter({ lat: Number(center?.lat), lng: Number(center?.lng) });
    // }

    setMap(map);
  }, []);

  const onUnmount = useCallback(function callback(
    map: google.maps.Map | undefined
  ) {
    setMap(undefined);
  },
  []);

  useEffect(() => {
    if (map) {
      const bounds = new google.maps.LatLngBounds();
      places.forEach(({ location: { lat, lng } }) => {
        bounds.extend({ lat: lat, lng: lng });
      });
      map.fitBounds(bounds);
    }
  }, [places, map]);

  const drawPolylines = (places: Place[]) => {
    const polylinesArray = [];
    const numDrifts = places.length;

    for (let i = 0; i < numDrifts - 1; i++) {
      const place = places[i];

      const nextPlace = places[i + 1] || undefined;

      if (!nextPlace) continue;

      const origin = place.location;
      const nextDestination = nextPlace.location;

      // For the first marker, connect it to the next marker and the deployment location
      // if (i === 0) {
      //   polylinesArray.push(
      //     <Polyline
      //       key={`polyline-${i}`}
      //       path={[origin, nextDestination]}
      //       options={MAP_SETTINGS.POLYLINE_OPTIONS.REGULAR}
      //     />
      //   );
      //   polylinesArray.push(
      //     <Polyline
      //       key={`polyline-${i}-to-deployment`}
      //       path={[
      //         {
      //           lat: Number(drifts[0].DeploymentLat),
      //           lng: Number(drifts[0].DeploymentLon),
      //         },
      //         origin,
      //       ]}
      //       options={MAP_SETTINGS.POLYLINE_OPTIONS.REGULAR}
      //     />
      //   );
      // }

      // For the last marker, connect it to the previous marker and the deployment location
      // if (i === numDrifts - 1) {
      //   polylinesArray.push(
      //     <Polyline
      //       key={`polyline-${i}-to-previous`}
      //       path={[origin, prevDestination]}
      //       options={MAP_SETTINGS.POLYLINE_OPTIONS.REGULAR}
      //     />
      //   );
      //   if (numDrifts > 1) {
      //     polylinesArray.push(
      //       <Polyline
      //         key={`polyline-${i}-to-deployment`}
      //         path={[
      //           origin,
      //           {
      //             lat: Number(drifts[0].DeploymentLat),
      //             lng: Number(drifts[0].DeploymentLon),
      //           },
      //         ]}
      //         options={MAP_SETTINGS.POLYLINE_OPTIONS.DASHED}
      //       />
      //     );
      //   }
      // }

      // if (i >= 0 && i < numDrifts) {
      polylinesArray.push(
        <Polyline
          key={`polyline-${i}`}
          path={[origin, nextDestination]}
          options={MAP_SETTINGS.POLYLINE_OPTIONS.REGULAR}
        />
      );
      <DistanceInfo key={`info-${i}`} from={place} to={nextPlace} />;

      // }
    }

    return polylinesArray;
  };

  return !isLoaded ? (
    <Loader />
  ) : (
    <GoogleMap
      mapContainerStyle={style}
      center={center}
      zoom={5}
      onLoad={onLoad}
      onUnmount={onUnmount}
      options={{
        styles: silverMapStyle,
        streetViewControl: false,
        scaleControl: true,
        mapTypeControl: false,
        panControl: false,
        zoomControl: false,
        rotateControl: false,
        fullscreenControl: true,
      }}
    >
      <div>
        {places.map((attraction) => (
          <MarkerF
            key={attraction.id}
            position={{
              lat: Number(attraction.location.lat),
              lng: Number(attraction.location.lng),
            }}
            icon={{
              url: `warning-marker.png`,
              scale: 1,
              scaledSize: new google.maps.Size(38, 38),
            }}
            onClick={() => onMarkerClick(attraction.id)}
          >
            {attraction.id === selected && (
              <InfoWindowF
                position={attraction.location}
                onCloseClick={() => onMarkerClick(null)}
                zIndex={99}
              >
                <p>{attraction.name}</p>
              </InfoWindowF>
            )}
          </MarkerF>
        ))}
      </div>
      {drawPolylines(places)}
    </GoogleMap>
  );
};

export default Map;
