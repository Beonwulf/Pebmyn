from flask import Blueprint, render_template
from flask_login import login_required
from flask_menu import register_menu
from App.Menus.sidebar import pebmynSideBar

pebmynSideBar.addSection(section='servermanagment', name='Hosting & Service', link='servermanagment')
pebmynSideBar.add(section='servermanagment', name='Tools & Settings', link='servermanagment.tools_settings', icon='wrench' )
pebmynSideBar.add(section='servermanagment', name='Extensions', link='servermanagment.sm_extensions', icon='tree' )
#pebmynSideBar.add(section='servermanagment', name='', link='servermanagment.' )

r_servermanagment = Blueprint('servermanagment', __name__, url_prefix='/ServerManagment')


@r_servermanagment.route('/')
@login_required
#@register_menu(servermanagment, '.servermanagment', 'Servermanagment')
def servermanagment_home():
    pass


@r_servermanagment.route('/ToolsSettings')
@login_required
#@register_menu(servermanagment, '.servermanagment.ToolsSettings', 'Tools & Settings')
def tools_settings():
    return render_template('servermanagment/tools_settings.html', menues=pebmynSideBar.get(), selected='servermanagment.tools_settings')


@r_servermanagment.route('/Extensions')
@login_required
#@register_menu(servermanagment, '.servermanagment.Extensions', 'Extensions')
def sm_extensions():
    return render_template('servermanagment/sm_extensions.html', menues=pebmynSideBar.get(), selected='servermanagment.sm_extensions')
