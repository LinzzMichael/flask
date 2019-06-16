from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
	openid  = StringField('openid', validators=[DataRequired()])#vaildators是检查器，这里配置的是检查是否数据为空
	remember_me = BooleanField('remember_me', default=False)