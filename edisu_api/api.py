from requests import Session
from .exceptions import CannotLogin

class API:
	__ORIGIN = 'https://edisuprenotazioni.edisu-piemonte.it'
	__URL_API = f'{__ORIGIN}:8443'

	def __init__(self) -> None:
		self.__req = Session()

		self.__req.headers = {
			'Origin': self.__ORIGIN,
			'Accept-Language': 'it'
		}

	def login(self, email: str, password: str) -> None:
		res_js = self.login_js_res(email, password)

		if res_js['status'] != 202:
			raise CannotLogin(res_js['message'])
		
		self.set_token(res_js['token'])

	def set_token(self, jwt_token) -> None:
		self.jwt_token: str = jwt_token
		self.__req.headers['Authorization'] = f"Bearer {self.jwt_token}"

	def login_js_res(self, email: str, password: str) -> dict:
		path = '/sbs/web/signin'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'email': email,
			'password': password
		}

		res_js = self.__req.post(
			req_url, data
		).json()

		return res_js
	
	def login_js_res_api_mobile(self, email: str, password: str) -> dict:
		path = '/sbs/users/signin'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'email': email,
			'password': password
		}

		res_js = self.__req.post(
			req_url, json = data
		).json()

		return res_js

	def get_consts(self) -> dict:
		path = '/sbs/web/master'
		req_url = f'{self.__URL_API}{path}'

		res_js = self.__req.post(
			req_url
		).json()

		return res_js

	def get_citylist_js_res_mobile(self) -> dict:
		path = '/sbs/booking/citylist'
		req_url = f'{self.__URL_API}{path}'

		res_js = self.__req.post(
			req_url
		).json()

		return res_js

	def get_study_rooms_js_res_mobile(self, id_city: int) -> dict:
		path = '/sbs/booking/halllist'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'city_id': id_city
		}

		res_js = self.__req.post(
			req_url, json = data
		).json()

		return res_js

	def get_study_rooms_js_res(self) -> dict:
		path = '/sbs/web/halllist'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'type': 0
		}

		res_js = self.__req.post(
			req_url, data
		).json()

		return res_js

	def get_study_room_bookings_data_js_res(self, id_study_room: int, date: str) -> dict:
		path = '/sbs/booking/bookingsperseats'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'hall_id': id_study_room,
			'date': date
		}

		res_js = self.__req.post(
			req_url, json = data
		).json()

		return res_js

	def set_custom_booking_data_js_res_mobile(
		self,
		id_study_room: int,
		date: str,
		start_time: str,
		end_time: str,
		id_seat: int
	) -> dict:
		path = '/sbs/booking/custombooking'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'hall_id': id_study_room,
			'date': date,
			'start_time': start_time,
			'end_time': end_time,
			'seat_id': id_seat
		}

		res_js = self.__req.post(
			req_url, json = data
		).json()

		return res_js

	def get_time_slots_js_res(self, study_room: str, id_study_room: int, date: str) -> dict:
		path = '/sbs/web/studentslots'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'date': date,
			'hall_id': f'{study_room} ({id_study_room})'
		}

		res_js = self.__req.post(
			req_url, data
		).json()

		return res_js

	def set_any_student_seat(
		self,
		date: str,
		study_room: str,
		id_study_room: int,
		time_start: str,
		time_end: str
	) -> dict:
		path = '/sbs/web/studentseatbook'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'date': date,
			'hall_id': f'{study_room} ({id_study_room})',
			'time_start': time_start,
			'time_end': time_end
		}

		res_js = self.__req.post(
			req_url, data
		).json()

		return res_js

	def get_booking_list_js_res_mobile(self) -> dict:
		path = '/sbs/booking/bookinglist'
		req_url = f'{self.__URL_API}{path}'

		data = {} # DON'T ASK ME WHY IT NEEDS AN EMPTY JSON

		res_js = self.__req.post(
			req_url, json = data
		).json()

		return res_js

	def get_user_info_js_res(self) -> dict:
		path = '/sbs/web/me'
		req_url = f'{self.__URL_API}{path}'

		res_js = self.__req.post(
			req_url
		).json()

		return res_js

	def book_cancel_js_res_mobile(self, id_booking: int) -> dict:
		path = '/sbs/booking/bookingcancel'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'booking_id': id_booking
		}

		res_js = self.__req.post(
			req_url, json = data
		).json()

		return res_js

	def book_cancel_js_res(self, id_booking: int) -> dict:
		path = '/sbs/web/bookingcancel'
		req_url = f'{self.__URL_API}{path}'

		data = {
			'booking_id': id_booking
		}

		res_js = self.__req.post(
			req_url, data
		).json()

		return res_js