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

#Role Status
	def _role_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

	def _role_status_display_2(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

	def _role_status_display_3(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

	def _role_status_display_4(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

	_name = "manage.role"
	_description = "Manage Roles"
	_columns = {
		'name': fields.char('Role', size=30, required=True),
		'status': fields.selection((('Created','Created'),('Active','Active'),('Deactivated','Deactivated'),('Blocked','Blocked')),'Status', required=True),
		'pages_actions_tab': fields.one2many('pages.actions', 'page_action_id', 'Pages & Actions'),
		'notification_tab': fields.one2many('notifications', 'notification_id', 'Notifications'),
		'documentation_tab': fields.one2many('documentations', 'documentation_id', 'Documentations'),
		'role_status_display_1': fields.function(_role_status_display_1, readonly=1, type='char'),
		'role_status_display_2': fields.function(_role_status_display_2, readonly=1, type='char'),
		'role_status_display_3': fields.function(_role_status_display_3, readonly=1, type='char'),
		'role_status_display_4': fields.function(_role_status_display_4, readonly=1, type='char'),
	}
create_users()

#EOF Create User
###############

class pages_actions(osv.osv):
	
	_name ='pages.actions'
	_description ="Pages & Actions"
	_columns = {
		'page_action_id' : fields.many2one('manage.role'),
		'name':fields.char('Items'),
		'view':fields.boolean('View'),
		'create':fields.boolean('Create'),
		'update':fields.boolean('Update'),
	}
pages_actions()

class notification(osv.osv):
	
	_name ='notifications'
	_description ="Notifications"
	_columns = {
		'notification_id' : fields.many2one('manage.role'),
		'name':fields.char('Items'),
		'active': fields.boolean('Active'),
	}
notification()

class documentations(osv.osv):
	
	_name ='documentations'
	_description ="Documentations"
	_columns = {
		'documentation_id' : fields.many2one('manage.role'),
		'name':fields.char('Items'),
		'generate': fields.boolean('Generate'),
		'receive': fields.boolean('Receive'),
	}
documentations()