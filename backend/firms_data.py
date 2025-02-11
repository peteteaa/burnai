import pandas as pd
import requests
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FirmsAPI:
    def __init__(self):
        self.map_key = "0efabb05c7274ef13eeb1270f4a50c99"  # Your FIRMS MAP_KEY
        self.base_url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
        self.max_retries = 3
        self.retry_delay = 10  # seconds

    def fetch_data_chunk(self, area, days):
        """
        Fetch a chunk of data for a specific number of days
        """
        url = f"{self.base_url}/{self.map_key}/VIIRS_SNPP_NRT/{area}/{days}"
        print(f"Requesting URL: {url}")
        
        for attempt in range(self.max_retries):
            try:
                print(f"Fetching data, attempt {attempt + 1}...")
                response = requests.get(url)
                response.raise_for_status()
                
                # Parse CSV data
                df = pd.read_csv(url)
                print(f"Retrieved {len(df)} records")
                return df
                
            except requests.exceptions.RequestException as e:
                if "429" in str(e) and attempt < self.max_retries - 1:  # Too Many Requests
                    print(f"Rate limit hit, waiting {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                print(f"Request error: {str(e)}")
                raise e
        return None

    def get_california_fires(self, total_days=30):
        """
        Fetch California fire data for the last n days
        Args:
            total_days (int): Total number of days to look back
        Returns:
            pandas.DataFrame: Filtered fire data
        """
        try:
            # California bounding box
            area = "-124,32,-114,42"  # lon_min,lat_min,lon_max,lat_max
            
            # Split into 10-day chunks
            chunks = []
            remaining_days = total_days
            
            while remaining_days > 0:
                days_to_fetch = min(10, remaining_days)
                chunk_df = self.fetch_data_chunk(area, days_to_fetch)
                
                if chunk_df is not None and not chunk_df.empty:
                    chunks.append(chunk_df)
                
                remaining_days -= days_to_fetch
                if remaining_days > 0:
                    print(f"Waiting before next request...")
                    time.sleep(5)  # Wait between chunks
            
            if not chunks:
                print("No data retrieved")
                return None
            
            # Combine all chunks
            df = pd.concat(chunks, ignore_index=True)
            
            # Filter for California
            df = df[
                (df['latitude'] > 32) & 
                (df['latitude'] < 42) & 
                (df['longitude'] > -124) & 
                (df['longitude'] < -114)
            ]
            
            # Select required columns
            result_df = df[['latitude', 'longitude', 'acq_date', 'frp']].copy()
            
            # Remove duplicates
            result_df = result_df.drop_duplicates()
            
            # Save to CSV in a data directory
            os.makedirs("data", exist_ok=True)
            output_file = os.path.join("data", f"california_fires_{datetime.now().strftime('%Y%m%d')}.csv")
            result_df.to_csv(output_file, index=False)
            print(f"Data saved to {output_file}")
            
            return result_df
            
        except Exception as e:
            print(f"Error fetching fire data: {str(e)}")
            return None

if __name__ == "__main__":
    # Initialize API
    firms = FirmsAPI()
    
    # Fetch last 30 days of fire data
    print("Fetching California fire data for the last 30 days...")
    df = firms.get_california_fires(total_days=30)
    
    if df is not None:
        print(f"\nFound {len(df)} fire incidents in California")
        print("\nFirst few records:")
        print(df.head())
        print(f"\nData columns: {df.columns.tolist()}")
    else:
        print("Failed to retrieve fire data") 