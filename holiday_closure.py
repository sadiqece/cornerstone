from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class holidays(osv.osv):
	_name = "holiday"
	_description = "This table is for keeping location data"
	_columns = {
		'holiday_id': fields.char('Id',size=20),
		'year': fields.selection((('2011','2011'),('2012','2012'),('2013','2013'),('2014','2014')),'Year'),
		'holiday_line': fields.one2many('holiday.line', 'holiday_line_id', 'Holiday Lines', select=True, required=True),
	}
holidays


class holiday_line(osv.osv):
	_name = "holiday.line"
	_description = "This table is for keeping location data"
	_columns = {
		'line_id': fields.char('Id',size=20),
		'description': fields.char('Description', size=100,required=True, select=True),
		'date_start': fields.date('Date Start'),
		'date_end': fields.date('Date End'),
		'holiday_line_id': fields.many2one('holiday', 'Holidays', ondelete='cascade', help='Holiday', select=True),
	}
holiday_line
