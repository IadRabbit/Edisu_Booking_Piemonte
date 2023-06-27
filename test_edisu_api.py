from pprint import pp
from edisu_api import API_SLIM, exceptions
from datetime import datetime, timedelta

from creds import email, passw

today_date = (datetime.today()+ timedelta(days=1)).strftime('%d-%m-%Y')

api_edisu = API_SLIM()

try:
	api_edisu.login(
		email = email,
		password = passw
	)
except exceptions.CannotLogin as e:
	print(e.res_js, e.msg)

def test_login_res():
	res = api_edisu.login_js_res(email, passw)
	print(res)


def test_study_rooms_res():
	#res = api_edisu.get_time_slots_js_res('MICHELANGELO', 1, today_date)
	#res = api_edisu.get_time_slots_js_res('MICHELANGELO', 1, today_date)
	#res = api_edisu.set_any_student_seat(today_date, 'MICHELANGELO', 2, '12:00', '12:30')
	#res = api_edisu.login_js_res_api_mobile(email, passw)
	res = api_edisu.book_cancel_js_res_mobile(1070793)
	pp(res)

#test_login_res()
test_study_rooms_res()

#pp(api_edisu.get_booking_list())
exit()
#api_edisu.book_cancel_js_res(api_edisu.get_last_booking()['id'])
last_book = api_edisu.pick_random_seat(1, today_date, '09:30', '10:30')
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
