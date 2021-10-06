#!/usr/bin/python3

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
import wtforms as m
from wtforms import validators as v
from wtforms.fields.html5 import DateField


# cannot use flask_upload, _uploads.uploaded_file is broken
# that photos.url() cannot be used, use flask instead
IMG = set('jpg jpe jpeg png gif svg bmp webp'.split())


class UserForm(FlaskForm):
    username = m.StringField('邮箱', validators=[
        v.input_required(), v.email('无效的邮箱地址')])
    password = m.PasswordField('密码', validators=[
        v.input_required(), v.length(min=4)])
    password2 = m.PasswordField('密码确认', validators=[
        v.input_required(), v.equal_to('password'), v.length(min=4)])
    address = m.StringField('地址', validators=[v.input_required()])
    submit = m.SubmitField('提交')


class LoginForm(FlaskForm):
    username = m.StringField('邮箱', validators=[
        v.input_required(), v.email()])
    password = m.PasswordField('密码', validators=[
        v.input_required(), v.length(min=4)])
    submit = m.SubmitField('提交')


class GoodsForm(FlaskForm):
    name = m.StringField('名称', validators=[v.input_required()])
    description = m.TextAreaField('描述', validators=[v.input_required()])
    # address for delivery
    address = m.StringField('地址', validators=[v.input_required()])
    no_bid = m.BooleanField('不讲价')
    original_price = m.FloatField('原价')
    lowest_price = m.FloatField('最低价', validators=[v.input_required()])
    highest_price = m.FloatField('最高价', validators=[v.input_required()])
    expired_date = DateField('截止时间')
    photo1 = FileField('照片1', validators=[FileAllowed(IMG, '不支持的格式')])
    photo2 = FileField('照片2', validators=[FileAllowed(IMG, '不支持的格式')])
    photo3 = FileField('照片3', validators=[FileAllowed(IMG, '不支持的格式')])
    submit = m.SubmitField('提交')
