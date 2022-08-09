from email.policy import default
from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, IntegerField, TextAreaField, BooleanField, FormField, DecimalField, SelectField, DateTimeField
from wtforms import validators
from .consts import condition_labels, comorbidity_labels, interface
from .set_network import Network, Time_Local

class LoginForm(Form):
    username = StringField('Username', [
        validators.length(min=3,max=50)
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])

class RegUserForm(Form):
    username = StringField('Username', [
        validators.length(min=3,max=50)
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=5),
        validators.EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirmar password')

class UserForm(Form):
    name = StringField('Nombre',[
        validators.length(max=50),
    ])
    phone = StringField('Telefono',[
        validators.length(max=10),
    ])
    email = EmailField('Correo',[
        validators.length(max=100),
        validators.Email()
    ])

class ConditionForm(Form):
    condi00 = BooleanField(condition_labels[0])
    condi01 = BooleanField(condition_labels[1])
    condi02 = BooleanField(condition_labels[2])
    condi03 = BooleanField(condition_labels[3])
    condi04 = BooleanField(condition_labels[4])
    condi05 = BooleanField(condition_labels[5])
    condi06 = BooleanField(condition_labels[6])
    condi07 = BooleanField(condition_labels[7])
    condi08 = BooleanField(condition_labels[8])
    condi09 = BooleanField(condition_labels[9])
    condi10 = BooleanField(condition_labels[10])
    condi11 = BooleanField(condition_labels[11])
    condi12 = BooleanField(condition_labels[12])
    condi13 = BooleanField(condition_labels[13])
    condi14 = BooleanField(condition_labels[14])

class ComorbidityForm(Form):
    cormo00 = BooleanField(comorbidity_labels[0])
    cormo01 = BooleanField(comorbidity_labels[1])
    cormo02 = BooleanField(comorbidity_labels[2])
    cormo03 = BooleanField(comorbidity_labels[3])
    cormo04 = BooleanField(comorbidity_labels[4])
    cormo05 = BooleanField(comorbidity_labels[5])
    cormo06 = BooleanField(comorbidity_labels[6])
    cormo07 = BooleanField(comorbidity_labels[7])
    cormo08 = BooleanField(comorbidity_labels[8])
    cormo09 = BooleanField(comorbidity_labels[9])
    cormo10 = BooleanField(comorbidity_labels[10])
    cormo11 = BooleanField(comorbidity_labels[11])
    cormo12 = BooleanField(comorbidity_labels[12])
    cormo13 = BooleanField(comorbidity_labels[13])
    cormo14 = BooleanField(comorbidity_labels[14])

class RegisterForm(Form):
    name = StringField('Nombre',[
        validators.length(max=50),
        validators.DataRequired()
    ])
    age = IntegerField('Edad',[
        validators.DataRequired(),
        validators.number_range(min=1, max=100)
    ], default=18)
    phone = StringField('Telefono',[
        validators.length(min =10, max=10),
        validators.DataRequired()
    ])
    email = EmailField('Correo',[
        validators.length(max=100),
        validators.DataRequired(),
        validators.Email()
    ])
    temperature = DecimalField('Temperatura',[
        validators.DataRequired(),
        validators.number_range(min=35.0, max=40.0)
    ], places=1, default=36.0)
    disease_chk = BooleanField('¿Tiene alguna enfermedad que aumente su temperatura corporal?')
    disease = StringField('¿Que enfermedad?', [
        validators.length(max=50)
    ])
    observations = TextAreaField('Sintomas u observaciones medicas', [
        validators.length(max=100),
        validators.DataRequired()
    ])
    other_chk = BooleanField('Otro')
    other = TextAreaField('¿Cual otra?', [
        validators.length(max=100)
    ])
    accept = BooleanField('Acepto terminos y condiciones', [
        validators.DataRequired()
    ])
    conditions = FormField(ConditionForm)
    comorbidities = FormField(ComorbidityForm)

class NetworkForm(Form):
    disabled = ''
    address = StringField('Direccion IP',[
        validators.DataRequired(),
        validators.IPAddress(),
    ], render_kw={disabled:''})
    netmask = StringField('Mascara de red',[
        validators.DataRequired(),
        validators.IPAddress(),
    ], render_kw={disabled:''})
    gateway = StringField('Puerta de enlace',[
        validators.DataRequired(),
        validators.IPAddress(),
    ], render_kw={disabled:''})
    #dhcp = BooleanField('DHCP', default= "checked")
    dhcp = SelectField('Enrutamiento', choices=[('dhcp','dhcp'),('static','static')])
    dns1 = StringField('DNS 1')
    dns2 = StringField('DNS 2')
    ssid = StringField('SSID')
    password = StringField('Password-SSID')

class DatetimeForm(Form):
    ntp = SelectField('Obtener automaticamente', choices=[('yes','Si'),('no','No')])
    dt = DateTimeField('Fecha y hora')
    zn = SelectField('Zona horaria', choices=Time_Local.get_timezones())

class ApForm(Form):
    status = SelectField('Punto de acceso (Hotspot)', choices=[('active','Activado'),('inactive','Desactivado')])
    ssid = StringField('AP_SSID')
    password = StringField('AP_PASSWORD')