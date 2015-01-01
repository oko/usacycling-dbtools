from libusac3.util import load_csv, RIDER_TRANSFORMS

rider_data = load_csv("wp_p_universal.csv", RIDER_TRANSFORMS)

from pprint import pprint
pprint(rider_data[0])