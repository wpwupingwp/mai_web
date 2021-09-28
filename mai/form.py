#!/usr/bin/python3

from flask_wtf import FlaskForm
import wtforms as m
from wtforms import validators as v


class UserForm(FlaskForm):
    username = m.StringField('邮箱', validators=[
        v.input_required(), v.email()])
    password = m.PasswordField('密码', validators=[
        v.input_required(), v.length(min=4)])
    password2 = m.PasswordField('密码确认', validators=[
        v.input_required(), v.equal_to('password'), v.length(min=4)])
    address = m.StringField('地址', validators=[v.input_required()])


class GoodsForm(FlaskForm):
    name = m.StringField('名称', validators=[v.input_required()])
    description = m.TextAreaField('描述', validators=[v.input_required()])
    # address for delivery
    address = m.StringField('地址', validators=[v.input_required()])
    no_bid = m.BooleanField('不讲价', validators=[v.input_required()])
    original_price = m.FloatField('原价')
    lowest_price = m.FloatField('最低价', validators=[v.input_required()])
    highest_price = m.FloatField('最高价', validators=[v.input_required()])
    expired_date = m.DateTimeField('截止时间')
    photo1 = m.FileField('照片')
    photo2 = m.FileField('照片')
    photo3 = m.FileField('照片')