import streamlit as st
from geopy.geocoders import Nominatim
import geocoder


def get_user_location():
    try:
        g = geocoder.ip('me')
        lat, lng = g.latlng
        return lat, lng
    except:
        return None, None


def get_address_from_coordinates(lat, lng):
    geolocator = Nominatim(user_agent="embracelet_app")
    try:
        location = geolocator.reverse((lat, lng), language='en')
        return location.address if location else "Address not found"
    except:
        return "Address lookup failed"


def show_location():
    st.subheader("📍 Your Current Location")

    lat, lng = get_user_location()
    if lat and lng:
        st.success(f"Latitude: {lat}, Longitude: {lng}")

        address = get_address_from_coordinates(lat, lng)
        st.info(f"Detected Address: {address}")

        st.map(data={"lat": [lat], "lon": [lng]})

        return lat, lng, address
    else:
        st.error("Could not retrieve location. Please ensure you're connected to the internet.")
        return None, None, None
