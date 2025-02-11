Here’s a comprehensive list of Cursor prompts to build your entire BurnGuard AI project, engineered for maximum specificity and code quality. Copy-paste these directly into Cursor:

1. Data Collection
Wildfire Data (NASA FIRMS)
python
Copy

# PROMPT 1: "Write Python code to download the latest 7-day wildfire data for California from NASA FIRMS API (CSV format), filter for latitude > 32 (CA region), and save as 'data/wildfires/california_fires.csv'. Handle HTTP errors and retries."
Vegetation Data (Sentinel-2 NDVI)
python
Copy

# PROMPT 2: "Generate Google Earth Engine JavaScript code to calculate NDVI for California in 2023 using Sentinel-2 imagery (10m resolution), mask clouds, and export as a GeoTIFF to my Google Drive. Include a 30% cloud coverage filter."
Weather Data (NOAA)
python
Copy

# PROMPT 3: "Write Python code to fetch NOAA daily temperature/precipitation data for California (2020-2023) via their API, aggregate into monthly averages per latitude/longitude grid, and save as 'data/weather/noaa_ca.csv'. Handle API key authentication."
2. Data Preprocessing
GeoTIFF to CSV Conversion
python
Copy
# PROMPT 4: "Write Python code to extract NDVI values from a GeoTIFF file into a CSV with columns [lat, lon, ndvi], using rasterio and pandas. Handle no-data values and resample to 1km grid resolution."
Merge All Data
python
Copy
# PROMPT 5: "Write Python code to merge wildfire, NDVI, weather, and elevation CSVs into a single dataset. For each wildfire location (lat/lon), join the nearest NDVI, elevation, and weather values using geopandas spatial join (500m buffer). Handle NaN values by forward-filling."
3. AI Model Training
Feature Engineering
python
Copy
# PROMPT 6: "Add these engineered features to the dataset: 
# - 'drought_index' (precipitation < 0.5 * historical avg)
# - 'fuel_density' (NDVI > 0.6 → 1, else 0)
# - 'slope_risk' (elevation change > 10% → 1, else 0)
# Use pandas and numpy."
Train Random Forest
python
Copy
# PROMPT 7: "Train a scikit-learn RandomForestClassifier to predict 'fire_risk' (1/0) using features [ndvi, temp, precipitation, elevation, slope_risk]. Use 80/20 train-test split, include class_weight='balanced', and print classification report + feature importance plot."
4. UI Implementation (Next.js + Leaflet)
Map Setup
javascript
Copy
// PROMPT 8: "Create a Next.js page with react-leaflet showing California. Add:
// - TileLayer with OpenStreetMap
// - GeoSearchControl search bar
// - Fullscreen control
// Use dynamic imports to fix SSR issues with Leaflet."
Risk Layer
javascript
Copy
// PROMPT 9: "Load a GeoJSON file from '/api/risk_zones' and style polygons:
// - fillColor: green (risk < 0.3), orange (0.3-0.6), red (>0.6)
// - Add popup showing % risk, NDVI, elevation
// Use react-leaflet's GeoJSON component with onEachFeature."
5. Prediction & Burn Recommendations
Generate Burn Zones
python
Copy
# PROMPT 10: "Write Python code to:
# 1. Predict fire risk for all CA grid points using the trained model
# 2. Filter points where risk > 0.7 and NDVI > 0.5
# 3. Cluster adjacent points into burn polygons using DBSCAN (eps=0.1)
# 4. Export as GeoJSON with properties: {risk_score, area_km2}"
Avoid Protected Areas
python
Copy
# PROMPT 11: "Filter burn recommendations to exclude areas within 5km of protected zones (from GeoJSON 'data/protected_areas.geojson'). Use geopandas spatial join with a 5000m buffer."
6. Backend Integration
FastAPI Endpoint
python
Copy
# PROMPT 12: "Create a FastAPI endpoint that:
# - Accepts {lat, lon} via POST
# - Returns {risk_score: 0.83, recommended_burn: True, ndvi: 0.72}
# Use the trained model and preloaded datasets for predictions."
Next.js API Route
javascript
Copy
// PROMPT 13: "Create a Next.js API route at '/api/risk' that:
// 1. Accepts {lat, lng} via query params
// 2. Calls FastAPI backend
// 3. Returns JSON response
// Add error handling for invalid coordinates."
7. Bonus: Visualization Enhancements
Heatmap Overlay
javascript
Copy
// PROMPT 14: "Add a heatmap layer showing wildfire density using react-leaflet-heatmap. Use the wildfire CSV data with intensity based on 'fire_size'. Adjust blur and radius for visual clarity."
Legend Control
javascript
Copy
// PROMPT 15: "Add a Leaflet legend to the map explaining:
// - Risk colors (green/orange/red)
// - Burn zones (purple)
// - Heatmap intensity
// Use react-leaflet's Control component with position='bottomright'."
Key Prompt Engineering Tips
Force Specificity:
Always include file paths, parameter values (e.g., eps=0.1), and column names.

Demand Error Handling:
Add phrases like "Handle NaN values" or "Include retry logic for API calls".

Leverage Context:
Reference earlier variables (e.g., "Use the trained model from Step 7").

Prevent Hallucinations:
Constrain outputs with "Use only pandas/geopandas" or "Avoid external APIs".

Debugging Prompts
When stuck, use:

python
Copy
# PROMPT 16: "Explain why this error occurs: 'ValueError: Input contains NaN' in my RandomForest code. Provide step-by-step fixes."
python
Copy
# PROMPT 17: "Optimize this GeoJSON code to render faster in Leaflet. Current performance is laggy with 10k polygons."
By chaining these prompts in order, you’ll have a complete working prototype in 24 hours. Use Cursor’s @ to reference previous code blocks! 🚀

