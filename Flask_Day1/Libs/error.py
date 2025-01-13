#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-09 16:16
# @Author  : skilywen

from flask import request, json
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    code = 500
    msg = 'sorry, 出了一些问题！'
    error_code = 999
    status = 1

    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None, status=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if status:
            self.status = status
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
                    status=self.status,
                    code=self.code,
                    msg=self.msg,
                    error_code=self.error_code,
                    request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None,  scope=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]


    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]