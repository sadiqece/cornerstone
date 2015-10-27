from dateutil import relativedelta
from openerp import addons

from functools import partial
import logging
import csv
from lxml import etree
from lxml.builder import E
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from datetime import datetime, timedelta, date
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
import openerp.exceptions
from openerp.osv import fields,osv, expression
from openerp.osv.orm import browse_record
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

####################
#User Management Page
####################

#Create User
###############

class create_users(osv.osv):

	_name = "manage.users"
	_description = "Settings"
	_columns = {
		'name': fields.char('Name', size=30, required=True),
		'login_name': fields.char('Login Name', size=30, required=True),
		'password': fields.char('Password', size=64,
			help="Keep empty if you don't want the user to be able to connect on the system."),
		'active': fields.boolean('Active:'),
		'login_date': fields.date('Latest connection', select=1),
		#'user_line': fields.one2many('user.module','qualify_id','Qualification'),
		#'users': fields.many2one('manage.users', 'Users', ondelete='cascade', help='Manage Users', select=True,required=True),
		#'user_group':fields.many2one('groups', 'User Group', required=True),
	}
	
	_defaults = {
		'active': True,
	}
	
create_users()

#EOF Create User
###############

####################
#User Group and Access Rights
####################

#Master class 
###############

class user_panel(osv.osv):

	def default_get(self, cr, uid, fields, context=None):

		data = super(user_panel, self).default_get(cr, uid, fields, context=context)
		invoice_lines = []

		modality_ids = self.pool.get('master.modules').search(cr, uid, [],limit=15)
		for p in self.pool.get('master.modules').browse(cr, uid, modality_ids):
			invoice_lines.append((0,0,{'module_list':p.id,}))
		data['user_line'] = invoice_lines
		return data
	
	def default_set(self, cr, uid, ids, fields, context=None):
	
		data = super(user_panel, self).read(cr, uid, ids, fields, context=context)
		csv_data = []
		out=open('security/ir.model.access.csv', 'rb')
		data=csv.reader(out)
		csv_data['user_line'] = data
		return data

	_name = "user.manage"
	_description = "Settings"
	_columns = {
	'user_group':fields.many2one('groups', 'User Group', required=True),
	'users': fields.many2one('manage.users', 'Users', ondelete='cascade', help='Manage Users', select=True,required=True),
	'user_line': fields.one2many('user.module','id','Qualification', readonly=1),
	'model_access': fields.one2many('ir.model.access', 'group_id', 'Access Controls'),
	}

	#_constraints = [(_class_start_notice, 'Error: Class Start Notice Cannot be Negative', ['Start Notice']),(_class_outstanding_notice, 'Error: Class Outstanding Notice Cannot be Negative', ['Outstanding Notice']),(_trainer_min_avail, 'Error: Trainer Min Avaliablity (%) Cannot be Negative', ['Avaliablity']),(_base_rate, 'Error: Base Rate ($ per hr) Cannot be Negative', ['Base Rate'])]
user_panel()


#Access Rights Class
###############
class assess_right(osv.osv):

	def read(self, cr, uid, ids, fields, context=None):
	
		data = super(assess_right, self).read(cr, uid, ids, fields, context=context)
		csv_data = []
		out=open('security/ir.model.access.csv', 'rb')
		data=csv.reader(out)
		csv_data['id'] = data
		csv_data['name'] = data
		csv_data['model_id:id'] = data
		csv_data['group_id:id'] = data
		csv_data['perm_read'] = data
		csv_data['perm_write'] = data
		csv_data['perm_create'] = data
		csv_data['perm_unlink'] = data
		return data
		
	_name = "user.module"
	_description = "User Access Rights"
	_columns = { 
	'qualify_id' : fields.many2one('user.manage', 'ID', ondelete='cascade', help='Test', select=True),
	#'module_list':fields.many2one('master.modules', 'Modules', ondelete='cascade', help='Modality', select=True, required=True),
	'id':fields.many2one('user.manage', 'ID', ondelete='cascade', help='Test', select=True),
	'name':fields.char('Name'),
	'model_id:id':fields.char('Model ID'),
	'group_id:id':fields.char('Group ID'),
	'perm_read':fields.boolean('Read'),
	'perm_write':fields.boolean('Write'),
	'perm_create':fields.boolean('Create'),
	'perm_unlink':fields.boolean('Delete'),
	}
		
assess_right()

class master_module(osv.osv):
		
	_name ='master.modules'
	_description ="Trainer Learner Tab"
	_columns = {
		'name':fields.char('Modules'),
	}
master_module()
	
class master_group(osv.osv):
	def _check_unique_group(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='groups'
	_description ="Manage Group"
	_columns = {
	'name':fields.char('User Group'),
	}
	_constraints = [(_check_unique_group, 'Error: Group Already Exists', ['Group'])]
master_group()

