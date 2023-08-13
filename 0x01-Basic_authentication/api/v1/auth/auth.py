#!/usr/bin/env python3
"""Create a class to handle authentication"""

from typing import List, TypeVar, Union
import re


class Auth:
    """A class to handle authentication APIs"""

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
        Check if auth is needed
        :param path: str
        :param excluded_paths: List[str]
        :return: bool = False for now
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if excluded_paths[-1] == '*':
            pat = excluded_paths.split('*')
            pat = pat[0] + '.*'
            match = re.search(pat, path)
            if match:
                return False
        if path[-1] != '/':
            path = path + '/'
        if path not in excluded_paths:
            return True
        else:
            return False

    def authorization_header(self, request=None) -> Union[str, None]:
        """
        header format
        :param request: object = flask request
        :return: str | None = None for now
        """
        if request is None:
            return None
        elif request.headers.get("Authorization"):
            return request.headers.get("Authorization")
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user's data
        :param request:
        :return:
        """
        return None
