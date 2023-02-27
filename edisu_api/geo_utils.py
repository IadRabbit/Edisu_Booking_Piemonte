from geopy.distance import distance
from geopy.geocoders import Nominatim

geo = Nominatim(
	user_agent = 'jslfagkghdlkglgdhlkghgdslk_sorry_my_cat_was_here'
)

def parse_location(address: str) -> dict[str, float]:
	street, city = address.split(' - ')
	cap, city = city.split(' ', 1)

	data = {
		'street': street,
		'city': city,
		'postalcode': cap
	}

	location = geo.geocode(data)
	#print(location.address)

	return {
		'lat': location.latitude,
		'long': location.longitude
	}

def calc_distance(
	point1: dict[str, float],
	point2: dict[str, float]
) -> float:
	return distance(
		point1.values(), point2.values()
	).km

def find_closest(
	point1: dict[str, float],
	addresses: list[str]
) -> tuple[
	float, dict[str, float]
]:
	address = addresses[0]
	coords = parse_location(address)

	min_distance = calc_distance(
		point1, coords
	)

	for c_address in addresses[1:]:
		c_coords = parse_location(c_address)

		c_distance = calc_distance(
			point1, c_coords
		)

		if c_distance < min_distance:
			min_distance = c_distance
			coords = c_coords
			address = c_address

	data = {
		'distance_km': min_distance,
		'coords': coords,
		'address': address
	}

	return data, addresses.index(address)