#!/usr/bin/env python3
"""New class to handle authentication
using the Basic architecture
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64


class BasicAuth(Auth):
	"""
	Class to handle basic authentication
	methods.
	"""

	def extract_base64_authorization_header(
			self, authorization_header: str) -> str:
		"""
		Extract the 'Base64' part of the header.
		:param authorization_header: Full header.
		:return: decoded base64 str
		"""
		if authorization_header and type(authorization_header) is str:
			if authorization_header.split()[0] == 'Basic':
				return authorization_header.split()[1]

	def decode_base64_authorization_header(
			self, base64_authorization_header: str) -> str:
		"""
		Decode base64
		:param base64_authorization_header: Incoming base64
		:return: converted string.
		"""
		if base64_authorization_header is not None and type(
				base64_authorization_header) is str:
			try:
				decoded = base64.b64decode(base64_authorization_header)
				return decoded.decode('utf-8')
			except Exception:
				return None
		return None

	def extract_user_credentials(self, decoded_base64_authorization_header: str
								 ) -> (str, str):
		"""
		Get username and password.
				Args:
					decoded_base64_authorization_header: str = decoded string
				Return: tuple(str, str) = a tuple containing the username
						and password.
		"""
		if decoded_base64_authorization_header:
			if type(decoded_base64_authorization_header) is str:
				content = decoded_base64_authorization_header.split(':', 1)
				if len(content) == 2:
					return (content[0], content[1])
		return (None, None)

	def user_object_from_credentials(self, user_email: str,
									 user_pwd: str) -> TypeVar('User'):
		"""
		Search through database with email and password to
		get user.
		Args:
				user_email: str = personnal email.
				user_pwd: str = extracted password.
		Return: user object.
		"""
		if user_email and user_pwd:
			if type(user_pwd) is str and type(user_email) is str:
				from models.user import User
				users = User.search({'email': user_email})
				if users:
					for user in users:
						if user.is_valid_password(user_pwd):
							return user
				return None
		return None

	def current_user(self, request=None) -> TypeVar('User'):
		"""
		Return the user who is making a request
		Args:
				request: str = the made request
		Return: user object.
		"""
		get_encoded_auth = self.authorization_header(request)
		if get_encoded_auth:
			get_encoded_str = self.extract_base64_authorization_header(
				get_encoded_auth)
		if get_encoded_str:
			get_decoded_str = self.decode_base64_authorization_header(
				get_encoded_str)
		if get_decoded_str:
			get_cred = self.extract_user_credentials(get_decoded_str)
		if get_cred:
			get_user = self.user_object_from_credentials(
				get_cred[0], get_cred[1])
			print(get_user)
			return get_user
		return None
