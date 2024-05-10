"""
    omer moshayov
    Locator Constants
"""

import subprocess
from constants import *
import googlemaps

# CONSTANTS
POWER_SHELL = "powershell.exe"
PATH = "C:\\Users\\yaniv\\loc.ps1" #סקריפט ב-powershell שמוצא נ"צ של מחשב


class Location_handler(object):
    """
    Handles the location of the PC
    """

    @staticmethod
    def location():
        """
        returns the location
        """
        try:
            f = open("Locator_copy.txt", "wb")
            p = subprocess.Popen([POWER_SHELL, PATH], stdout = f) # מריץ את הסקריפט בשורת הפקודה של הפאוורשל
            p.communicate()
            f.close()
            f1 = open("Locator_copy.txt", "rb")
            txt = f1.read().decode()
            f1.close()
            return txt
        except Exception as e:
            print("general error", e)

    @staticmethod
    def get_lat_lon():
        """
        returns the location as a string which contains
        the latitude and the longitude
        """
        loc = Location_handler.location()
        lst = loc.split()
        print(lst)
        loc_lst = [SECOND, THIRD]
        lat = lst[4]
        lon = lst[5]
        loc_lst[0] = lat
        loc_lst[1] = lon
        datum_point = lat + " " + lon
        print(datum_point)
        return datum_point

    @staticmethod
    def turn_to_address(loc):
        """
        turn the lat and lon to an address
        """
        lst = loc.split()
        lat = lst[FIRST]
        lon = lst[SECOND]
        gmaps = googlemaps.Client(key=API_KEY)
        reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
        return reverse_geocode_result[FIRST]["formatted_address"]

    @staticmethod
    def create_map(address):
        """
        gets the address of the location and creates
        a map with the location.
        :param address: the address of the location
        """
        location = Location_handler.turn_to_address(address)
        gmaps = googlemaps.Client(key=API_KEY)
        locations = [location]
        markers = ["color:dark black|size:extra large|label:" + chr(65 + i) + "|" + r for i, r in enumerate(locations)]
        result_map = gmaps.static_map(
            center=location,
            scale=2,
            zoom=17,
            size=[640, 640],
            format="jpg",
            maptype="roadmap",
            markers=markers,
            path="color:0x0000ff|weight:2|" + "|".join(location))
        with open("location_map.jpg", 'wb') as img:
            for chunk in result_map:
                img.write(chunk)
        return True


def main():
    Location_handler.create_map(Location_handler.get_lat_lon())


if __name__ == "__main__":
    main()