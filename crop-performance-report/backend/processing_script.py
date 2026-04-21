# processing_script.pyTWILIO_ACCOUNT_SID = "YOUR_TWILIO_SID" # Replace with your full SID
#TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"  
# processing_script.py

# import ee
# from twilio.rest import Client
# import datetime

# # --- API CREDENTIALS AND CONFIGURATION ---
# # IMPORTANT: Replace with your actual credentials.


# # --- Google Earth Engine Initialization ---
# try:
#     ee.Initialize(project='crop-monitoring-project')
#     print("Google Earth Engine authenticated successfully.")
# except Exception as e:
#     print(f"Error initializing Google Earth Engine: {e}")
#     print("Please check your project setup and authentication.")
#     exit()

# # --- CORE FUNCTIONS ---

# def analyze_farm_health(lon, lat):
#     """
#     Analyzes crop health for a specific location using Google Earth Engine.
#     """
#     print(f"Analyzing location: Lon={lon}, Lat={lat}")
#     farm_point = ee.Geometry.Point([lon, lat])
#     aoi = farm_point.buffer(500).bounds()

#     end_date = datetime.datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=90)

#     image_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
#               .filterBounds(aoi) \
#               .filterDate(start_date, end_date) \
#               .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#               .sort('CLOUDY_PIXEL_PERCENTAGE')
    
#     if image_collection.size().getInfo() == 0:
#         print("No cloud-free image found for the given period.")
#         return None

#     image = image_collection.first()

#     ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

#     stats = ndvi.reduceRegion(
#         reducer=ee.Reducer.mean(),
#         geometry=aoi,
#         scale=10
#     ).get('NDVI').getInfo()

#     if stats is None:
#         print("Could not calculate statistics for the area. It might be over water.")
#         return None

#     print(f"Calculated Average NDVI: {stats:.4f}")
#     return stats

# def generate_status_message(ndvi_value):
#     """
#     Creates a simple text report based on the NDVI value.
#     """
#     if ndvi_value is None:
#         return "Report Error: Could not analyze the selected location."

#     if ndvi_value < 0.2:
#         status = "No Vegetation Detected"
#         details = "The selected area does not appear to be a farm."
#     elif ndvi_value < 0.4:
#         status = "Attention Needed"
#         details = "Low vegetation detected. Please check your field."
#     elif ndvi_value < 0.7:
#         status = "Moderate Growth"
#         details = "Your crop is stable. Continue to monitor."
#     else:
#         status = "Good Growth"
#         details = "Your crop is healthy and growing well."
    
#     return f"Weekly Crop Report\nStatus: {status}\nNDVI Value: {ndvi_value:.2f}\nDetails: {details}"

# def send_sms_alert(message_body):
#     """
#     Sends an SMS using the Twilio API.
#     """
#     try:
#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#         message = client.messages.create(
#             body=message_body,
#             from_=TWILIO_PHONE_NUMBER,
#             to=FARMER_PHONE_NUMBER
#         )
#         print(f"SMS sent successfully! SID: {message.sid}")
#     except Exception as e:
#         print(f"Error sending SMS via Twilio: {e}")

# # This part only runs if you execute this script directly for testing
# if __name__ == '__main__':
#     print("--- Starting Manual Test Run ---")
#     farm_longitude = 77.35
#     farm_latitude = 16.20
#     avg_ndvi = analyze_farm_health(farm_longitude, farm_latitude)
#     report_message = generate_status_message(avg_ndvi)
#     print("\n--- Generated Report ---")
#     print(report_message)
#     print("------------------------\n")
#     send_sms_alert(report_message)
#     print("\n--- Manual Test Run Complete. ---")


import ee
from twilio.rest import Client
import datetime

# --- API CREDENTIALS AND CONFIGURATION ---
# IMPORTANT: Replace with your actual credentials.
# Note: Your credentials were included in the prompt. It's recommended to use environment variables for security.
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_TOKEN"
TWILIO_PHONE_NUMBER = "+13135131191"
FARMER_PHONE_NUMBER = "YOUR_PHONE_NUMBER"

# --- Google Earth Engine Initialization ---
try:
    ee.Initialize(project='crop-monitoring-project')
    print("Google Earth Engine authenticated successfully.")
except Exception as e:
    print(f"Error initializing Google Earth Engine: {e}")
    print("Please check your project setup and authentication.")
    exit()

# --- CORE FUNCTIONS ---
def analyze_farm_health(lon, lat):
    """
    Analyzes crop health for a specific location using a cloud-free composite
    from Google Earth Engine.
    """
    print(f"Analyzing location: Lon={lon}, Lat={lat}")
    farm_point = ee.Geometry.Point([lon, lat])
    aoi = farm_point.buffer(500).bounds()

    # --- FIX APPLIED HERE ---
    # Instead of using today's date (which is set in the future),
    # we hard-code a valid date range from the past for testing.
    # This ensures real satellite data will be found. 📅
    start_date = '2024-06-01'
    end_date = '2024-08-31'

    image_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                         .filterBounds(aoi) \
                         .filterDate(start_date, end_date) \
                         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50))

    if image_collection.size().getInfo() == 0:
        print("No images found for the given period, even with high cloud cover.")
        return None

    image = image_collection.median()

    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

    stats = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=10
    ).get('NDVI').getInfo()

    if stats is None:
        print("Could not calculate statistics for the area. It might be over water or data is sparse.")
        return None

    print(f"Calculated Average NDVI: {stats:.4f}")
    return stats
# def analyze_farm_health(lon, lat):
#     """
#     Analyzes crop health for a specific location using a cloud-free composite
#     from Google Earth Engine.
#     """
#     print(f"Analyzing location: Lon={lon}, Lat={lat}")
#     farm_point = ee.Geometry.Point([lon, lat])
#     aoi = farm_point.buffer(500).bounds() # Area of Interest: 500-meter buffer

#     # Define a 90-day window for analysis, which is a good balance
#     end_date = datetime.datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=90)

#     # --- IMPROVEMENT ---
#     # Instead of picking one image, we create a single, high-quality composite image.
#     # The .median() method takes all images in the date range and calculates the
#     # median pixel value, which effectively removes clouds and other noise.
#     image_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
#                          .filterBounds(aoi) \
#                          .filterDate(start_date, end_date) \
#                          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50)) # Loosen filter slightly

#     # Check if there are any images at all, even cloudy ones, to create a composite from.
#     if image_collection.size().getInfo() == 0:
#         print("No images found for the given period, even with high cloud cover.")
#         return None

#     # Create a single, cloud-free composite image from the collection.
#     image = image_collection.median()

#     # Calculate NDVI (Normalized Difference Vegetation Index)
#     # NDVI = (NIR - Red) / (NIR + Red)
#     # For Sentinel-2, NIR is band B8 and Red is band B4.
#     ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

#     # Calculate the average NDVI value within the farmer's area of interest.
#     stats = ndvi.reduceRegion(
#         reducer=ee.Reducer.mean(),
#         geometry=aoi,
#         scale=10 # 10-meter resolution for Sentinel-2
#     ).get('NDVI').getInfo()

#     if stats is None:
#         print("Could not calculate statistics for the area. It might be over water or data is sparse.")
#         return None

#     print(f"Calculated Average NDVI: {stats:.4f}")
#     return stats

def generate_status_message(ndvi_value):
    """
    Creates a simple text report based on the NDVI value.
    """
    if ndvi_value is None:
        return "Report Error: Could not analyze the selected location. This may be due to persistent heavy cloud cover."

    # NDVI ranges from -1 to +1. Higher values mean healthier vegetation.
    if ndvi_value < 0.2:
        status = "Poor Health / Barren"
        details = "Very low or no vegetation detected. Field may be fallow, recently planted, or under stress."
    elif ndvi_value < 0.4:
        status = "Attention Needed"
        details = "Vegetation health is below average. Check for issues like pests, water stress, or nutrient deficiency."
    elif ndvi_value < 0.7:
        status = "Moderate Growth"
        details = "Your crop shows stable, moderate growth. Continue to monitor and maintain standard practices."
    else:
        status = "Excellent Growth"
        details = "Your crop is healthy and vigorous. Growth is well above average. Keep up the good work!"
    
    return f"Weekly Crop Report\nStatus: {status}\nNDVI Value: {ndvi_value:.2f}\nDetails: {details}"

def send_sms_alert(message_body):
    """
    Sends an SMS using the Twilio API.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=FARMER_PHONE_NUMBER
        )
        print(f"SMS sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS via Twilio: {e}")

# This part only runs if you execute this script directly for testing
if __name__ == '__main__':
    print("--- Starting Manual Test Run ---")
    # Coordinates for Raichur, Karnataka
    farm_longitude = 77.35
    farm_latitude = 16.20
    avg_ndvi = analyze_farm_health(farm_longitude, farm_latitude)
    report_message = generate_status_message(avg_ndvi)
    print("\n--- Generated Report ---")
    print(report_message)
    print("------------------------\n")
    send_sms_alert(report_message)
    print("\n--- Manual Test Run Complete. ---")