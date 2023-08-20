export const MAP_SETTINGS = {
  DEFAULT_MAP_OPTIONS: {
    scrollwheel: false,
    mapTypeControl: false,
    fullscreenControl: false,
    streetViewControl: false,
  },
  DEFAULT_CENTER: { lat: 57, lng: 20 },
  DEFAULT_ZOOM: 4,
  MARKER_SIZE: {
    SMALL: 18,
    LARGE: 25,
  },
  PIXEL_OFFSET: {
    X: 0,
    Y: 10,
  },
  POLYLINE_OPTIONS: {
    DASHED: {
      geodesic: true,
      strokeOpacity: 0,
      strokeWeight: 2,
      strokeColor: "#247291",
      icons: [
        {
          icon: {
            path: "M 0,0 0,1",
            strokeOpacity: 1,
            strokeWeight: 2,
            scale: 3,
          },
          repeat: "10px",
        },
      ],
    },
    REGULAR: {
      geodesic: true,
      strokeOpacity: 1,
      strokeWeight: 2,
      strokeColor: "#fada5e",
    },
  },
};
