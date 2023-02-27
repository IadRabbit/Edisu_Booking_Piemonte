from pprint import pp
from edisu_api import API_SLIM
from datetime import datetime, timedelta

email = 'email'
passw = 'pass'
today_date = datetime.today().strftime('%d-%m-%Y')

api_edisu = API_SLIM()

api_edisu.login(
	email = email,
	password = passw
)

#pp(api_edisu.get_study_room_booking_data_choices(1, today_date, '19:00', '00:00')[:40])
#api_edisu.book_cancel_js_res(api_edisu.get_last_booking()['id'])
last_book = api_edisu.set_custom_booking_data_js_res_mobile(1, today_date, '02:30', '08:30', 40)
print(last_book)
exit()
last_book = api_edisu.get_consts()
pp(last_book)
for b in api_edisu.get_booking_list()[:3]:
	pp(b)
#pp(last_book)
exit()
#pp(api_edisu.book_cancel_js_res(last_book['id']))
res = api_edisu.get_citylist()
id_city = res[0]['id_city']
rooms = api_edisu.get_study_rooms(id_city)
pp(rooms)
#exit()
id_room = rooms[0]['id']
room = rooms[0]['name']
res = api_edisu.get_study_room_booking_data_js_res(id_room, today_date)
pp(res)
res = api_edisu.reserve_place_all_cost_by_study_room(room, id_room, today_date)
pp(res)
