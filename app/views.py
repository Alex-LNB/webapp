from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import login_manager
from .forms import ApForm, LoginForm, RegUserForm, UserForm, RegisterForm, NetworkForm, DatetimeForm
from .models import User, Person, Condi, Comorbidity
from .set_network import AccessPoint, Network, Time_Local
from .consts import interface

page = Blueprint('page',__name__)

@page.before_app_first_request
def before_req():
    User.set_admin()
    Condi.set_default()
    Comorbidity.set_default()

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)

@page.route('/')
@page.route('/index')
def index():
    return render_template('index.html', title='Index') # Se devuelve el html renderizado y se envia 'title' que contiene el titulo de la pagina

@page.route('/form', methods=['GET','POST']) # Se establece el metodo GET por default, se asigna POST para obtener los valores del formulario
def form():
    form = RegisterForm(request.form) # Se crea una instancia del formulario, se le asigna request.form para obtener los valores al recibir la peticion POST
    if request.method == 'POST' and form.validate(): # Se valida que la peticion sea POST y que las validaciones del formulario sean correctas
        if form.disease_chk.data: # Se verifica el primer check del formulario y se asigna el valor correspondiente
            disease_temp = form.disease.data
        else:
            disease_temp = 'No'
        # Se crea una instancia del modelo Person, que crea un registro en la BD
        per = Person.create_element(name=form.name.data, 
                                    age=form.age.data, 
                                    phone=form.phone.data, 
                                    email=form.email.data, 
                                    temperature=form.temperature.data, 
                                    disease_temp=disease_temp, 
                                    observations=form.observations.data)
        for x in form.conditions: # Ciclo que valida el check de cada Condición y hace la relacion con la instancia Person creada
            if x.data:
                lab = f'{x.label}'
                condi = Condi.get_by_label(lab[32:-8]) # Se parte el label para quitar las etquetas html
                Person.set_condi(per.id, condi)
        for y in form.comorbidities: # Ciclo que valida el check de cada Comorbilidad y hace la relacion con la instancia Person creada
            if y.data:
                lad = f'{y.label}'
                comor = Comorbidity.get_by_label(lad[35:-8]) # Se parte el label para quitar las etquetas html
                Person.set_comor(per.id, comor)
        if form.other_chk.data: # Se verifica el check de 'otro' y si existe se da de alta en la BD y se asigna a la instancia Person creada
            comor = Comorbidity.create_element(form.other.data)
            Person.set_comor(per.id, comor)        
        flash('Registro exitoso') # Se envia el mensaje de exito
        return redirect(url_for('.index')) # Redirecciona a Index
    return render_template('register/form.html', title='Form', form=form) # Se devuelve el html renderizado y se envia 'title' que contiene el titulo de la pagina, 'form' que contiene el formulario

@page.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.lista'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(f'Iniciaste sesion {user.username}')
            return redirect(url_for('.lista'))
        else: 
            flash('Usuario y/o contraseña invalidos', 'error')
            return redirect(url_for('.login'))
    return render_template('auth/login.html', title='Login', form=form)

@page.route('/register', methods=['GET','POST'])
@login_required
def register():
    form = RegUserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.create_element(form.username.data, form.password.data)
        flash(f'Usuario {user.username} creado')
        return redirect(url_for('.register'))
    return render_template('auth/register.html', title='Register', form=form)

@page.route('/user/<int:user_id>')
@login_required
def show_user(user_id):
    user = User.get_by_id(user_id)
    return render_template('auth/show_user.html', title='User', user=user)    

@page.route('/user/edit/<int:user_id>', methods=['GET','POST'])
@login_required
def edit_user(user_id):
    user = User.get_by_id(user_id)
    if not (current_user.id == user.id or current_user.is_admin):
        flash('No tiene permiso para editar este usuario')
        return redirect(url_for('.lista'))
    form = UserForm(request.form, obj=user)
    if request.method == 'POST' and form.validate():
        user = User.update_element(user.id,form.name.data,form.phone.data,form.email.data)
        if user:
            flash(f'Usuario {user.username} actualizado')
    return render_template('auth/user_edit.html', title='Edit User', form=form, user=user)

@page.route('/list')
@page.route('/list/<int:page>')
@login_required
def lista(page=1, per_page=5):
    pagination = Person.get_all(page, per_page)
    pers = pagination.items
    return render_template('register/list.html', title='Lista', pers=pers, pagination=pagination, page=page)

@page.route('/logout')
def logout():
    logout_user()
    flash('Cerraste session')
    return redirect(url_for('.login'))

@page.route('/setdate', methods=['GET','POST'])
@login_required
def setdate():
    if not current_user.is_admin:
        flash('No tiene permisos de administrador')
        redirect(url_for('.lista'))
    dtl = Time_Local.get_timelocal()
    form = DatetimeForm(request.form, obj=dtl)
    if request.method == 'POST' and form.validate():
        msj = Time_Local.set_timelocal(form.ntp.data,form.dt.data,form.zn.data)
        flash(f'{msj}')
        return redirect(url_for('.setdate'))
    return render_template('config/setdate.html', title='Datetime', form=form, dtl=dtl)

@page.route('/setnet', methods=['GET','POST'])
@login_required
def setnet():
    if not current_user.is_admin:
        flash('No tiene permisos de administrador')
        redirect(url_for('.lista'))
    ap = AccessPoint.get_ap()
    form = ApForm(request.form, obj=ap)
    ethe = Network.get_net(interface=interface['ether'])
    wifi = Network.get_net(interface=interface['wifi'], wifi=True)
    if request.method == 'POST':
        buff = AccessPoint.set_ap(form.status.data)
        y, z= Network.apply_netplan()
        flash(f'{buff} - {y}')
        return redirect(url_for('.setnet'))
    return render_template('config/setnet.html', title='Network', form=form, ethe=ethe, wifi=wifi)

@page.route('/setnet/ethernet', methods=['GET','POST'])
@login_required
def setethe():
    if not current_user.is_admin:
        flash('No tiene permisos de administrador')
        redirect(url_for('.lista'))
    net = Network.get_net(interface=interface['ether'])
    form = NetworkForm(request.form, obj=net)
    if request.method == 'POST' and form.validate():
        if form.dhcp.data == 'dhcp':
            x = Network.upnet_dhcp(interface=interface['ether'])
        elif form.dhcp.data == 'static':
            x = Network.upnet_static(interface=interface['ether'], address=form.address.data, netmask=form.netmask.data, gateway=form.gateway.data, dns1=form.dns1.data, dns2=form.dns2.data)
        if x == 0:
            y, z= Network.apply_netplan()
            flash(f'Configuracion de red actualizada - {y}')
            return redirect(url_for('.lista'))
        else:
            flash(f'Fallo la configuracion de red - {y}','error')
            return redirect(url_for('.lista'))
    return render_template('config/setethe.html', title='Ethernet', net=net, form=form)

@page.route('/setnet/wifi', methods=['GET','POST'])
@login_required
def setwifi():
    if not current_user.is_admin:
        flash('No tiene permisos de administrador')
        redirect(url_for('.lista'))
    net = Network.get_net(interface=interface['wifi'],wifi=True)
    form = NetworkForm(request.form, obj=net)
    if request.method == 'POST' and form.validate():
        if form.dhcp.data == 'dhcp':
            x = Network.upnet_dhcp(interface=interface['wifi'], wifi=True, ssid=form.ssid.data, password=form.password.data)
        elif form.dhcp.data == 'static':
            x = Network.upnet_static(interface=interface['wifi'], address=form.address.data, netmask=form.netmask.data, gateway=form.gateway.data, dns1=form.dns1.data, dns2=form.dns2.data, wifi=True, ssid=form.ssid.data, password=form.password.data)
        if x == 0:
            y, z= Network.apply_netplan()
            flash(f'Configuracion de red actualizada - {y}')
            return redirect(url_for('.lista'))
        else:
            flash(f'Fallo la configuracion de red - {y}','error')
            return redirect(url_for('.lista'))
    return render_template('config/setwifi.html', title='Wifi', net=net, form=form)