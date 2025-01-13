#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-09 16:03
# @Author  : skilywen
from wtforms import Form
from flask import request
import html
import json
from werkzeug.exceptions import HTTPException
import sys
from Libs.error_code import ParametersException

class BaseForm(Form):
    def __init__(self):
        data = html.escape(request.data.decode(), quote=False)
        data = json.loads(data)
        kwargs = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **kwargs)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # raise HTTPException(self.errors)
            raise ParametersException()
        return self