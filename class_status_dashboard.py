from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class class_status_dashboard_info(osv.osv):
	_name = "class.status.dashboard.info"
	_description = "This table is for keeping Test Schedules"
	_columns = {
	
	}
class_status_dashboard_info()