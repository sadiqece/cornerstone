import datetime
from dateutil import relativedelta
from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools	
import re
import base64
from content_index_learner import cntIndex
from openerp.tools.misc import ustr


_logger = logging.getLogger(__name__)

class generate_reports(osv.osv):

	_name = "generate.reports"
	_description = "Reports"
	_columns = {
		'name': fields.char('Name', size=30, readonly=1),
	}
	
	_defaults = { 
	   'name': 'Charles Report',
	}
	#_constraints = [(_class_start_notice, 'Error: Class Start Notice Cannot be Negative', ['Start Notice']),(_class_outstanding_notice, 'Error: Class Outstanding Notice Cannot be Negative', ['Outstanding Notice']),(_trainer_min_avail, 'Error: Trainer Min Avaliablity (%) Cannot be Negative', ['Avaliablity']),(_base_rate, 'Error: Base Rate ($ per hr) Cannot be Negative', ['Base Rate'])]
generate_reports()