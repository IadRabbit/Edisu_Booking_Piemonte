from datetime import datetime
from edisu_api import API_SLIM
from edisu_api.geo_utils import parse_location, calc_distance, find_closest

email = 'email'
passw = 'pass'
today_date = datetime.today().strftime('%d-%m-%Y')

api_edisu = API_SLIM(
	email = email,
	password = passw
)

study_rooms = api_edisu.get_study_rooms_location(1)

dist1 = {
	'lat': 45.075647,
	'long': 7.602805
}

print(find_closest(dist1, study_rooms))