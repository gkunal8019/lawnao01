import requests
import google_image
import json

url = "https://app.regrid.com/api/v1/search.json?query="


def get_image(address):
    """
    The `get_image` function takes an address as input, makes a request to an API to retrieve data for
    that address, and returns an image, total square footage, house area, and coordinates if successful.

    :param address: The `address` parameter is a string that represents the address of a location
    :return: The function `get_image` returns a tuple containing the following values:
    - `image`: The image obtained from the `getimage_google` function.
    - `total_sqft`: The total square footage of the property.
    - `house_area`: The square footage of the house area.
    - `coordinates`: The coordinates of the property.
    """
   
    addresses = []
    addresses.append(address)
    headers = {
        "accept": "application/json",
        "x-regrid-token": "CtORtUj73e9LN9SrJOq9rqvKxe09dVpYrARh0OA3JfN6VsOaTLffcvYJXi9uIN4L"
       # "x-regrid-token": "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNjk5MTA5NjAxLCJleHAiOjE3MDE3MDE2MDEsInUiOjM0ODI1NCwiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnNiIn0.XTrxpe-kPxzpj909P9HrGvnNLEFpkGaVMrrfVs2gOIk",
    }
    house_areas = []
    for count, address in enumerate(addresses, start=23):
        params = {"query": address}

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            try:
                coordinates = data["results"][0]["geometry"]["coordinates"][0]

                file_name, timestamp, google_image_url = google_image.getimage_google(
                    coordinates
                )
                try:
                    total_sqft = data["results"][0]["properties"]["fields"]["sqft"]
                except:
                    try:
                        total_sqft = data["results"][0]["properties"]["fields"][
                            "ll_gissqft"
                        ]
                    except:
                        total_sqft = 0
                try:
                    house_area = data["results"][0]["properties"]["fields"][
                        "ed_bldg_footprint_sqft"
                    ]
                except:
                    try:
                        house_area = data["results"][0]["properties"]["fields"][
                            "ll_bldg_footprint_sqft"
                        ]
                    except:
                        house_area = 0
                with open ('data.json','w') as json_file:
                    json.dump(data,json_file)

                return (
                    file_name,
                    timestamp,
                    total_sqft,
                    house_area,
                    coordinates,
                    google_image_url,
                )

            except Exception as e:
                return e

        else:
            return f"Error getting data for {address}: {response.status_code}"

