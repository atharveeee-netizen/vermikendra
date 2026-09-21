'use client';

import { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Bin, Field } from '../types';
import Link from 'next/link';

// Custom icons based on status
const createIcon = (color: string) => new L.Icon({
  iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const icons = {
  NORMAL: createIcon('green'),
  WATCH: createIcon('yellow'),
  ACTION_NEEDED: createIcon('red'),
  OFFLINE: createIcon('grey'),
  UNKNOWN: createIcon('blue')
};

interface FarmMapProps {
  fields: Field[];
  bins: Bin[];
}

function MapUpdater({ bins, fields }: FarmMapProps) {
  const map = useMap();
  useEffect(() => {
    if (bins.length === 0 && fields.length === 0) return;
    
    const bounds = L.latLngBounds([]);
    let hasCoords = false;

    bins.forEach(bin => {
      if (bin.latitude && bin.longitude) {
        bounds.extend([bin.latitude, bin.longitude]);
        hasCoords = true;
      }
    });

    fields.forEach(field => {
      if (field.boundary) {
        try {
          const geo = JSON.parse(field.boundary);
          if (geo.coordinates && geo.coordinates[0]) {
             geo.coordinates[0].forEach((coord: number[]) => {
                 // GeoJSON is [lon, lat], Leaflet is [lat, lon]
                 bounds.extend([coord[1], coord[0]]);
                 hasCoords = true;
             });
          }
        } catch (e) {
          // ignore parsing errors
        }
      }
    });

    if (hasCoords) {
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [bins, fields, map]);

  return null;
}

export default function FarmMap({ fields, bins }: FarmMapProps) {
  return (
    <MapContainer 
      center={[18.520, 73.856]} 
      zoom={13} 
      className="w-full h-full z-0"
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {fields.map(field => {
        if (!field.boundary) return null;
        try {
           const geo = JSON.parse(field.boundary);
           const latLngs = geo.coordinates[0].map((coord: number[]) => [coord[1], coord[0]]);
           return (
             <Polygon 
               key={field.id} 
               positions={latLngs} 
               pathOptions={{ color: '#2d7a42', fillColor: '#2d7a42', fillOpacity: 0.2 }}
             >
               <Popup>
                 <div className="font-bold text-slate-800 uppercase tracking-wider">{field.name}</div>
               </Popup>
             </Polygon>
           );
        } catch(e) {
           return null;
        }
      })}

      {bins.map(bin => {
        if (!bin.latitude || !bin.longitude) return null;
        const icon = icons.NORMAL; 
        return (
          <Marker 
            key={bin.id} 
            position={[bin.latitude, bin.longitude]}
            icon={icon}
          >
            <Popup className="vermikendra-popup">
              <div className="flex flex-col gap-2 min-w-[150px]">
                <div>
                  <h3 className="font-black text-slate-800 uppercase tracking-tighter text-sm">{bin.name}</h3>
                  <span className="text-[10px] font-bold uppercase tracking-widest text-[#2d7a42] bg-green-50 px-1 py-0.5 rounded">NORMAL</span>
                </div>
                <Link 
                  href={`/bed/${bin.id}`}
                  className="bg-slate-900 text-white text-xs font-bold uppercase tracking-wider text-center py-2 rounded shadow-md active:scale-95 transition-transform"
                >
                  View Details
                </Link>
              </div>
            </Popup>
          </Marker>
        );
      })}
      
      <MapUpdater bins={bins} fields={fields} />
    </MapContainer>
  );
}
