from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired


class LoginForm(Form):
    # openid = StringField('openid', validators=[DataRequired()])
    state = SelectField('state', choices=[('DC', 'District Of Columbia'),('MD', 'Maryland'),('NC','North Carolina'),
                                          ('SC','South Carolina'),('VA','Virginia'),('WV','West Virginia')])
    indicator = SelectField('indicator', choices=[('GDP','GDP'),('TotalPersonalIncome','TotalPersonalIncome'),
                                                  ('HousePriceIndex','HousePriceIndex'),('UnemploymentRate','UnemploymentRate')])
    newArray = []
    for i in range(2009,2025):
        newArray.append((i,i))
    startyear = SelectField('startyear', choices=newArray)
    nextyear = SelectField('nextyear', choices=newArray)    
# remember_me = BooleanField('remember_me', default=False)
