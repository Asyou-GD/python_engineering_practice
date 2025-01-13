#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-09 15:16
# @Author  : skilywen

from wtforms import Form
from wtforms.validators import DataRequired,Regexp
from wtforms import StringField, IntegerField
from flask_wtf import FlaskForm
from validators.Base import BaseForm

class SingleDetailForm(BaseForm):
    vul_detection_id = StringField('vul_detection_id', validators=[DataRequired('不允许为空')])


class WebStartForm(BaseForm):
    ip = StringField('ip', validators=[DataRequired('不允许为空')])
    port = IntegerField('port', validators=[DataRequired('不允许为空')])

class StartScriptForm(BaseForm):
    match_name = StringField('match_name',validators = [DataRequired('不允许为空')])

class UserForm(BaseForm):
    username = StringField('username', validators = [DataRequired('不允许为空')])
    password = StringField('password', validators = [DataRequired('不允许为空')])
    image_code = StringField('image_code', validators = [DataRequired('不允许为空')])
    uid = StringField('uid', validators = [DataRequired('不允许为空')])

class DetectionForm(BaseForm):
    test_id = StringField('test_id', validators = [DataRequired('不允许为空')])