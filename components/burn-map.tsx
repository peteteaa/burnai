/// <reference types="@types/google.maps" />

"use client"

import { useEffect, useRef, useState } from "react"
import { Loader } from "@googlemaps/js-api-loader"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Compass, Plus, Minus, Layers } from "lucide-react"

// Define the burn potential types
type BurnPotential = {
  location: google.maps.LatLng
  value: number // 0-1, where 0 is safe (green) and 1 is high burn potential (red)
}

export default function BurnMap() {
  const mapRef = useRef<HTMLDivElement>(null)
  const map = useRef<google.maps.Map | null>(null)
  const heatmap = useRef<google.maps.visualization.HeatmapLayer | null>(null)
  const searchBox = useRef<google.maps.places.SearchBox | null>(null)
  const [searchInput, setSearchInput] = useState("")

  useEffect(() => {
    console.log("Starting map initialization...")
    console.log("API Key:", process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY)
    
    const initMap = async () => {
      try {
        const loader = new Loader({
          apiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? "",
          version: "weekly",
          libraries: ["places", "visualization"],
          channel: "next-js",
          retries: 3,
          language: "en",
          region: "US",
        })

        console.log("Loading Google Maps...")
        const google = await loader.load()
        console.log("Google Maps loaded successfully")

        if (!mapRef.current) {
          console.error("Map container ref is null")
          return
        }

        // Initialize the map
        map.current = new google.maps.Map(mapRef.current, {
          center: { lat: 37.7749, lng: -122.4194 }, // San Francisco
          zoom: 13,
          mapTypeControl: false,
          fullscreenControl: false,
          streetViewControl: false,
          styles: [
            {
              featureType: "poi",
              elementType: "labels",
              stylers: [{ visibility: "off" }],
            },
          ],
        })
        console.log("Map initialized successfully")

        // Initialize the search box
        const input = document.getElementById("map-search") as HTMLInputElement | null
        if (!input) {
          console.error("Search input element not found")
          return
        }
        console.log("Found search input element:", input)
        
        try {
          searchBox.current = new google.maps.places.SearchBox(input)
          console.log("Search box initialized successfully")
        } catch (error) {
          console.error("Error initializing search box:", error)
          return
        }

        // Bias the SearchBox results towards current map's viewport
        if (map.current) {
          map.current.addListener("bounds_changed", () => {
            if (searchBox.current && map.current) {
              searchBox.current.setBounds(map.current.getBounds() as google.maps.LatLngBounds)
            }
          })
        }

        // Listen for the event fired when the user selects a prediction
        if (searchBox.current) {
          searchBox.current.addListener("places_changed", () => {
            const places = searchBox.current?.getPlaces()
            if (!places?.length) return

            const bounds = new google.maps.LatLngBounds()
            places.forEach((place) => {
              if (!place.geometry) {
                console.log("Returned place contains no geometry")
                return
              }

              if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport)
              } else if (place.geometry.location) {
                bounds.extend(place.geometry.location)
              }

              // Create a marker for the selected place
              new google.maps.Marker({
                map: map.current,
                title: place.name,
                position: place.geometry.location,
              })
            })

            // Fit the map to show all markers and the selected area
            map.current?.fitBounds(bounds)
            map.current?.setZoom(Math.min(map.current?.getZoom() || 14, 14)) // Don't zoom in too far
          })
        }

        // Initialize heatmap layer
        heatmap.current = new google.maps.visualization.HeatmapLayer({
          map: map.current,
          data: [],
          gradient: ["rgba(0, 255, 0, 0)", "rgba(0, 255, 0, 1)", "rgba(255, 255, 0, 1)", "rgba(255, 0, 0, 1)"],
        })
      } catch (error) {
        console.error("Error initializing map:", error)
      }
    }

    initMap()
    
    return () => {
      // Cleanup
      if (map.current) {
        // @ts-ignore
        map.current = null
      }
    }
  }, [])

  // Example function to update burn potential data
  const updateBurnPotentialData = (data: BurnPotential[]) => {
    if (heatmap.current) {
      const heatmapData = data.map((point) => ({
        location: point.location,
        weight: point.value,
      }))
      heatmap.current.setData(heatmapData)
    }
  }

  return (
    <div className="h-screen w-full relative" style={{ height: '100vh', width: '100%' }}>
      {/* Search bar */}
      <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-[9999] w-full max-w-md px-4" style={{ pointerEvents: 'auto' }}>
        <div className="relative w-full bg-white rounded-full shadow-xl">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 h-5 w-5 z-10" />
          <Input
            id="map-search"
            className="w-full pl-10 pr-4 py-3 rounded-full border-0 bg-white focus:ring-2 focus:ring-blue-500"
            placeholder="Search any location..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            autoComplete="off"
          />
        </div>
      </div>

      {/* Map controls */}
      <div className="absolute right-4 bottom-24 z-10 flex flex-col gap-2">
        <Button variant="default" size="icon" className="rounded-full bg-white text-black hover:bg-gray-100">
          <Compass className="h-4 w-4" />
        </Button>
        <div className="flex flex-col bg-white rounded-full shadow">
          <Button variant="ghost" size="icon" className="rounded-full">
            <Plus className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="rounded-full">
            <Minus className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Layers control */}
      <div className="absolute left-4 bottom-24 z-10">
        <Button variant="default" size="icon" className="rounded-full bg-white text-black hover:bg-gray-100">
          <Layers className="h-4 w-4" />
        </Button>
      </div>

      {/* Map container */}
      <div 
        ref={mapRef} 
        className="h-full w-full"
        style={{ 
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          height: '100%',
          width: '100%'
        }} 
      />
    </div>
  )
}

