import datetime
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
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
import openerp.exceptions
from openerp.osv import fields,osv, expression
from openerp.osv.orm import browse_record
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class users_profile(osv.osv):

#Image
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		#raise osv.except_osv(_('Warning!'),_('dddddd %s')%(123456))
		return self.pool.get('learner.info').write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		'''obj_write = self.pool.get('learner.info')
		for i in pay_recs:
			vals = {
				'image': i[0],
				'cost': i[1],
				'pay_id': iid
			}
			obj_pay.create(cr, uid, vals)
		
		return True
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)'''

#User Status
	def _user_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

	def _user_status_display_2(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

	def _user_status_display_3(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

	def _user_status_display_4(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['status']
		return res

#dob
	def months_between(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
		
	def onchange_dob(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.datetime.now().date()))
			res = {'value':{}}
			if d < 0:
				res['value']['birth_date'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, future date not allowed.')}})
				return res
			return dob
			
	'''def create(self, cr, uid, vals, context=None):
		user_obj = self.pool.get('res.users')
		vals_user = {
			'user_name': vals.get('name'),
			'login': default_login,
			#other required field 
		}
		user_obj.create(cr, uid, vals_user, context)
		result = super(users_profile, self).create(cr, uid, vals, context=context)
		return result'''
		
	def _check_unique_user_profile_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.user_profile_id == self_obj.user_profile_id and x.name == self_obj.name:
						raise osv.except_osv(_('Error:'),_('"Name as in NRIC" already exist')%(self_obj))
		return True
		
	_name ='user.profiles'
	_description ="User Profile"
	_columns = {
		'user_profile_id' : fields.integer('User Profile ID', size=200),
		'name':fields.char('Name as in NRIC', size=30, required=True),
		'sur_name':fields.char('Surname', size=20),
		'given_name':fields.char('Title', size=20, required=True),
		'name_nric':fields.char('Name', size=20, required=True),
		'user_name':fields.char('User Name', size=20, required=True),
		'password':fields.char('Password', size=20, required=True),
		'status': fields.selection((('Created','Created'),('Active','Active'),('Deactivated','Deactivated'),('Blocked','Blocked')),'Status', required=True),
		'role': fields.many2one('manage.role', 'Role', ondelete='cascade', help='Role', select=True),
		'profile_pages_actions_tab': fields.one2many('profile.pages.actions', 'page_action_id', 'Pages & Actions'),
		'profile_notification_tab': fields.one2many('profile.notifications', 'notification_id', 'Notifications'),
		'profile_documentation_tab': fields.one2many('profile.documentations', 'documentation_id', 'Documentations'),
		'profile_history_tab': fields.one2many('profile.history', 'history_id', 'History'),
		'user_status_display_1': fields.function(_user_status_display_1, readonly=1, type='char'),
		'user_status_display_2': fields.function(_user_status_display_2, readonly=1, type='char'),
		'user_status_display_3': fields.function(_user_status_display_3, readonly=1, type='char'),
		'user_status_display_4': fields.function(_user_status_display_4, readonly=1, type='char'),
		'nationality':fields.selection((('Singapore','Singapore'),('Malaysia','Malaysia'),('South Korea','South Korea'),('North Korea','North Korea'),('India','India'),('Indonesia','Indonesia'),('Vietnam','Vietnam')),'Nationality',required=True),
		'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
		'race':fields.many2one('user.race', 'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'addr_1': fields.char('Address Line 1'),
		'addr_2': fields.char('Address Line 2'),
		'postal_code': fields.char('Postal Code', size=6),
		'unit_no': fields.integer('Unit Number', size=9),
		'mobile_no': fields.integer('Mobile Number', size=9),
		'landline_no': fields.integer('Home/Office Number', size=9),
				'image': fields.binary("Photo",
            help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized photo", type="binary", multi="_get_image",
            store = {
                'learner.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the employee. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Smal-sized photo", type="binary", multi="_get_image",
            store = {
                'learner.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized photo of the employee. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
	}
	_constraints = [(_check_unique_user_profile_name, 'Error: Name as in NRIC already exist', ['NRIC'])]
	_defaults = {
		'nationality': 'Singapore',
	}
users_profile()

class master_race1(osv.osv):
	def _check_unique_race(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='user.race'
	_description ="User Profile Race"
	_columns = {
	'name':fields.char('Race'),
	}
	_constraints = [(_check_unique_race, 'Error: Race Already Exists', ['Race'])]
master_race1()

class profile_pages_actions(osv.osv):
	
	_name ='profile.pages.actions'
	_description ="Pages & Actions"
	_columns = {
		'page_action_id' : fields.many2one('user.profiles', 'Page Action ID', ondelete='cascade', help='Learner', select=True),
		'profile_items':fields.char('Items'),
		'view':fields.boolean('View'),
		'create':fields.boolean('Create'),
		'update':fields.boolean('Update'),
	}
profile_pages_actions()

class profile_notification(osv.osv):
	
	_name ='profile.notifications'
	_description ="Notifications"
	_columns = {
		'notification_id' : fields.many2one('user.profiles', 'Notifications ID', ondelete='cascade', help='Learner', select=True),
		'notification_items':fields.char('Items'),
		'active': fields.boolean('Active'),
	}
profile_notification()

class profile_documentations(osv.osv):
	
	_name ='profile.documentations'
	_description ="Documentations"
	_columns = {
		'documentation_id' : fields.many2one('user.profiles', 'Documentations ID', ondelete='cascade', help='Learner', select=True),
		'documentation_items':fields.char('Items'),
		'generate': fields.boolean('Generate'),
		'receive': fields.boolean('Receive'),
	}
profile_documentations()

class profile_history(osv.osv):
	
	_name ='profile.history'
	_description ="Personal History"
	_columns = {
		'history_id' : fields.many2one('user.profiles', 'History ID', ondelete='cascade', help='Learner', select=True),
		'history_items':fields.char('Items'),
	}
profile_history()















