from random import choice
from datetime import datetime, timedelta

from .api import API
from .exceptions import PossibleClosedStudyRoom

class API_SLIM(API):
	def get_citylist(self) -> list[
		dict[str, int | str]
	]:
		js_res = self.get_citylist_js_res_mobile()

		citylist = [
			{
				'id_city': city['id'],
				'city': city['name']
			}
			for city in js_res['result']['data']['list']
		]

		return citylist

	def get_study_rooms(self, id_city: int) -> list[
		dict[str, str | int]
	]:
		js_res = self.get_study_rooms_js_res_mobile(id_city)

		study_rooms = [
			study_room
			for study_room in js_res['result']['data']['list']
		]

		return study_rooms

	def get_booking_list(self) -> list[dict]:
		js_res = self.get_booking_list_js_res_mobile()

		booking_list = [
			booking_data
			for booking_data in js_res['result']['slots']
		]

		return booking_list

	def get_last_booking(self) -> dict:
		booking_list = self.get_booking_list()

		return booking_list[0]

	def get_user_info(self) -> dict:
		user_data = self.get_user_info_js_res()['result']['data']

		return user_data

	def get_study_rooms_location(self, id_city: int) -> list[str]:
		js_res = self.get_study_rooms_js_res_mobile(id_city)

		return self.only_location(js_res)
		
	@staticmethod
	def only_location(js_res: dict):
		study_rooms = [
			study_room['location']
			for study_room in js_res['result']['data']['list']
		]

		return study_rooms

	@staticmethod
	def get_status_booking():
		STATUS_BOOKING = {
			0: 'Canceled',
			1: 'Upcoming',
			2: 'Completed',
			4: 'Pending'
		}

		return STATUS_BOOKING

	def get_study_room_location(self, id_city: int, id_study_room: int):
		js_res = self.get_study_rooms_js_res_mobile(id_city)
		location = None

		for study_room in js_res['result']['data']['list']:
			if study_room['id'] == id_study_room:
				location = study_room['location']
				break

		return location

	def get_time_slots(self, study_room: str, id_study_room: int, date: str) -> list[dict]:
		js_res = self.get_time_slots_js_res(
			study_room, id_study_room, date
		)

		if not 'result' in js_res:
			raise PossibleClosedStudyRoom('No data found, possible study room closed or internal error, their api sucks a bit I know')

		return js_res['result']['data']['list']

	def get_user_booking(self, id_booking: str) -> dict:
		booking_list = self.get_booking_list()

		for booking in booking_list:
			if booking['id'] == id_booking:
				break

		return booking

	def get_study_room_bookings_data(self, id_study_room: int, date: str) -> dict:
		js_res = self.get_study_room_bookings_data_js_res(
			id_study_room, date
		)

		return js_res['result']['seats']

	def get_study_room_booking_data_choices(
		self,
		id_study_room: int,
		date: str,
		start_time: str,
		end_time: str
	) -> list[dict]:
		bookings_data = self.get_study_room_bookings_data(id_study_room, date)
		time_start = datetime.strptime(start_time, '%H:%M')
		time_end = datetime.strptime(end_time, '%H:%M')

		if time_end.hour == 0 and time_end.minute == 0:
			time_end += timedelta(minutes = -1, days = 1)

		seats_avalaible = []

		def get_seats(bookings_data: list[dict]):
			for booking_data in bookings_data:
				is_ok = True

				if 'booked_time' in booking_data:
					for time_bookend in booking_data['booked_time']:
						c_time_start = datetime.strptime(time_bookend['time_start'], '%H:%M')
						c_time_end = datetime.strptime(time_bookend['time_end'], '%H:%M')

						if c_time_end.hour == 0 and c_time_end.minute == 0:
							c_time_end += timedelta(minutes = -1, days = 1)

						if (
							(
								time_start <= c_time_start < time_end
							) or (
								time_start < c_time_end <= time_end
							) or (
								c_time_start <= time_start < c_time_end
							) or (
								c_time_start < time_end <= c_time_end
							)
						):
							is_ok = False
							break

				if is_ok:
					seats_avalaible.append(booking_data)

		get_seats(bookings_data[10:-10])

		if not seats_avalaible:
			get_seats(bookings_data)

		return seats_avalaible

	def pick_random_seat(
		self,
		id_study_room: int,
		date: str,
		start_time: str,
		end_time: str
	) -> dict:
		seats_avalaible = self.get_study_room_booking_data_choices(id_study_room, date, start_time, end_time)
		
		if not seats_avalaible:
			return

		the_chosen_one = choice(seats_avalaible)

		res_js = self.set_custom_booking_data_js_res_mobile(
			id_study_room, date,
			start_time, end_time, the_chosen_one['id']
		)

		return res_js