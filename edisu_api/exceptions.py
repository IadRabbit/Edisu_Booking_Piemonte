class CannotLogin(Exception):
	def __init__(self, msg: str, res_js: dict) -> None:
		self.res_js = res_js
		self.msg = msg

		super().__init__(msg)

class PossibleClosedStudyRoom(Exception):
	def __init__(self, msg: str) -> None:
		self.msg = msg

		super().__init__(msg)