from flask import Blueprint, render_template
from flask_login import login_required
from flask_menu import register_menu
from App.Menus.sidebar import pebmynSideBar


pebmynSideBar.addSection(section='hostingservices', name='Hosting & Service', link='hostingservices')
pebmynSideBar.add(section='hostingservices', name='Resellers', link='hostingservices.resellers', icon='user-tie' )
pebmynSideBar.add(section='hostingservices', name='Customers', link='hostingservices.customers', icon='user' )
pebmynSideBar.add(section='hostingservices', name='Domains', link='hostingservices.domains', icon='earth' )

r_hostingservices = Blueprint('hostingservices', __name__, url_prefix='/HostingServices')


@r_hostingservices.route('/')
@login_required
#@register_menu(hostingservices, '.hostingservices', 'Hosting Services')
def hostingservices_home():
    return render_template('hostingservices/index.html', menues=pebmynSideBar.get(), selected='hostingservices.home')


@r_hostingservices.route('/Resellers')
@login_required
#@register_menu(hostingservices, '.hostingservices.Resellers', 'Resellers')
def resellers():
    return render_template('hostingservices/resellers.html', menues=pebmynSideBar.get(), selected='hostingservices.resellers')


@r_hostingservices.route('/Customers')
@login_required
#@register_menu(hostingservices, '.hostingservices.Customers', 'Customers')
def customers():
    return render_template('hostingservices/customers.html', menues=pebmynSideBar.get(), selected='hostingservices.customers')


@r_hostingservices.route('/Domains')
@login_required
#@register_menu(hostingservices, '.hostingservices.Domains', 'Domains')
def domains():
    return render_template('hostingservices/domains.html', menues=pebmynSideBar.get(), selected='hostingservices.domains')
