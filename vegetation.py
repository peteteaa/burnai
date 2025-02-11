import ee

# Initialize the Earth Engine module
ee.Initialize(project="heroic-gantry-450601-j7")

# Define the region of interest (California boundary)
california = ee.FeatureCollection("TIGER/2018/States").filter(ee.Filter.eq("NAME", "California"))

# Function to mask clouds and shadows using the SCL band (Scene Classification Layer)
def mask_clouds(image):
    scl = image.select("SCL")  # SCL (Scene Classification Layer) band
    mask = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10))  # Remove clouds, shadows, cirrus
    return image.updateMask(mask)

# Load Sentinel-2 imagery for 2023, filter by region, date, and cloud coverage
s2_collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(california)
    .filterDate("2023-01-01", "2023-12-31")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30))  # Apply 30% cloud coverage filter
    .map(mask_clouds)
)

# Ensure the collection is not empty
count = s2_collection.size().getInfo()
if count == 0:
    raise ValueError("No Sentinel-2 images found for the given filters. Try adjusting the date or region.")

# Calculate NDVI (Normalized Difference Vegetation Index)
def compute_ndvi(image):
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return image.addBands(ndvi)

# Apply NDVI calculation to each image in the collection
ndvi_collection = s2_collection.map(compute_ndvi)

# Reduce the collection to a median composite
ndvi_median = ndvi_collection.select("NDVI").median()

# Define export parameters
export_task = ee.batch.Export.image.toDrive(
    image=ndvi_median,
    description="California_NDVI_2023",
    folder="GEE_Exports",
    fileNamePrefix="california_ndvi_2023",
    region=california.geometry(),
    scale=10,
    maxPixels=1e13,
    fileFormat="GeoTIFF"
)

# Start the export task
export_task.start()

print("Export started. Check Google Drive for output.")
