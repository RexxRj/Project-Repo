import React, { useRef, useEffect } from "react";

import "./Map.css";

const Map = (props) => {
  const L = window.L;
  const MapRef = useRef();

  const { center, zoom } = props;

  useEffect(() => {
    const map = L.map(MapRef.current).setView(
      [props.center.lat, props.center.lng],
      props.zoom
    );

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    const marker = L.marker([props.center.lat, props.center.lng]).addTo(map);
  }, [center, zoom]);

  return (
    <div
      ref={MapRef}
      className={`map ${props.className}`}
      style={props.style}
    ></div>
  );
};

export default Map;
