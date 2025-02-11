import ee

# Initialize Earth Engine
ee.Initialize(project="heroic-gantry-450601-j7")

# Define the region of interest (San Francisco County)
san_francisco = ee.FeatureCollection("TIGER/2018/Counties").filter(ee.Filter.eq("NAME", "San Francisco"))

# Function to mask clouds
def mask_clouds(image):
    scl = image.select("SCL")
    mask = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10))
    return image.updateMask(mask)

# Load and filter Sentinel-2 images
s2_collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(san_francisco)
    .filterDate("2023-06-01", "2023-07-31")  # Reduced date range
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))  # Stricter cloud filter
    .map(mask_clouds)
)

# Check if images exist
if s2_collection.size().getInfo() == 0:
    raise ValueError("No Sentinel-2 images found for San Francisco. Adjust filters.")

# Compute NDVI
def compute_ndvi(image):
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return image.addBands(ndvi)

ndvi_collection = s2_collection.map(compute_ndvi)
ndvi_reduced = ndvi_collection.select("NDVI").mean()  # Use mean instead of median

# Export with reduced size parameters
export_task = ee.batch.Export.image.toDrive(
    image=ndvi_reduced,
    description="SanFrancisco_NDVI",
    folder="GEE_Exports",
    fileNamePrefix="sanfrancisco_ndvi",
    region=san_francisco.geometry(),
    scale=30,  # Adjust resolution
    maxPixels=1e10,
    fileFormat="GeoTIFF"
)

export_task.start()
print("Export started for San Francisco. Check Google Drive.")
print("Export status:", export_task.status())
