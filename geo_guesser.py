import requests
from time import sleep

# Cloudflare datacenter locations with their codes
datacenters = {
    "AMS": "Amsterdam, Netherlands",
    "ATL": "Atlanta, USA",
    "BLR": "Bangalore, India",
    "BOM": "Mumbai, India",
    "DFW": "Dallas, USA",
    "FRA": "Frankfurt, Germany",
    "HKG": "Hong Kong, China",
    "IAD": "Washington, DC, USA",
    "ICN": "Seoul, South Korea",
    "JFK": "New York, USA",
    "LAX": "Los Angeles, USA",
    "LHR": "London, UK",
    "MEL": "Melbourne, Australia",
    "SGP": "Singapore",
    "SYD": "Sydney, Australia",
    "TOR": "Toronto, Canada",
    "VIE": "Vienna, Austria",
    "ZRH": "Zurich, Switzerland",
    "SAO": "Sao Paulo, Brazil",
    "KHI": "Karachi, Pakistan",  # Karachi datacenter
    # Add more if needed
}

# List of Cloudflare datacenters for cfteleport
cfteleport_datacenters = [
    "FRA", "KHI", "KHI", "AMS", "ATL", "BLR", "BOM", "DFW", "FRA", "HKG",
    "IAD", "ICN", "JFK", "LAX", "LHR", "MEL", "SGP", "SYD", "TOR", "VIE",
    "ZRH", "SAO", "KHI"
]

# URL of the Discord CDN image
discord_image_url = "https://cdn.discordapp.com/attachments/1330148451530309695/1335231234737049640/images.png?ex=679f6a7d&is=679e18fd&hm=2ab22a6bef145a5499351ba152377f8ba560d878ee9b2bfb99b6050b4e1b6bf1&"

# List of retries in case of timeout
max_retries = 3
retry_delay = 0  # seconds

# Simulated headers to avoid blocking by Cloudflare
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


# Function to check the image in every Cloudflare datacenter using cfteleport
def check_image_in_datacenters(image_url):
    for datacenter in cfteleport_datacenters:
        retries = 0
        while retries < max_retries:
            try:
                # Build the cfteleport URL with the proxy and colo parameters
                cfteleport_url = f"https://cfteleport.xyz/?proxy={image_url}&colo={datacenter}"
                print(cfteleport_url)
                # Send the request to the image URL via cfteleport
                response = requests.get(
                    cfteleport_url, headers=headers,
                    timeout=10)  # Increased timeout to 10 seconds

                # Extract CF-Ray header to get the datacenter code
                cf_ray_header = response.headers.get("CF-Ray")

                if cf_ray_header:
                    # The datacenter code is after the last dash in the CF-Ray header
                    datacenter_code = cf_ray_header.split("-")[-1]

                    # Check if the datacenter code matches any known datacenter
                    if datacenter_code in datacenters:
                        print(
                            f"Image found in datacenter: {datacenters[datacenter_code]} (CF-Ray: {cf_ray_header})"
                        )
                    else:
                        print(
                            f"Datacenter code {datacenter_code} not found in the list."
                        )
                else:
                    print(
                        f"No CF-Ray header found for datacenter {datacenter}.")

                break
            except requests.exceptions.Timeout:
                retries += 1
                print(
                    f"Timeout error for {datacenter}. Retrying {retries}/{max_retries}..."
                )
                sleep(retry_delay)  # Wait before retrying
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to {datacenter}: {e}")
                break  # Break on other types of errors


# Test the function
check_image_in_datacenters(discord_image_url)
