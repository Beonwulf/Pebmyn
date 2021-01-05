from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from App.Menus.sidebar import pebmynSideBar


pebmynSideBar.addSection('main', 'Main')
pebmynSideBar.add(section='main', name='Home', link='main.index', icon='home' )
pebmynSideBar.add(section='main', name='Dashboard', link='main.dashboard', icon='fire' )
r_main = Blueprint('main', __name__)


@r_main.route('/')
#@register_sidebar('main', 'Home', '')
#@register_menu(r_main, '.main', 'Home', order=0, icon='home')
def index():
    sbm = {}
    if current_user.is_active:
        sbm = pebmynSideBar.get()
    else:
        return redirect(url_for('auth.login'))
    return render_template('index.html', menues=sbm, selected='main.index')


@r_main.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', menues=pebmynSideBar.get(), selected='main.dashboard')


@r_main.route('/profile')
# @register_menu(r_main, '.main.profile', 'Profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username, menues=pebmynSideBar.get(), selected='main.profile')
