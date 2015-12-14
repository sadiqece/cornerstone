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

	_name = "manage.role"
	_description = "Manage Roles"
	_columns = {
		'name': fields.char('Name', size=30, required=True),
		'status': fields.selection((('Active','Active'),('InActive','InActive'),('Blocked','Blocked')),'Status', required=True),
		'pages_actions_tab': fields.one2many('pages.actions', 'page_action_id', 'Pages & Actions'),
		'notification_tab': fields.one2many('notifications', 'notification_id', 'Notifications'),
		'documentation_tab': fields.one2many('documentations', 'documentation_id', 'Documentations'),
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
	}
notification()

class documentations(osv.osv):
	
	_name ='documentations'
	_description ="Documentations"
	_columns = {
		'documentation_id' : fields.many2one('manage.role'),
		'name':fields.char('Items'),
	}
documentations()

class users_profile(osv.osv):

	#Image
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		#raise osv.except_osv(_('Warning!'),_('dddddd %s')%(123456))
		return self.pool.get('user.profiles').write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
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
	
	_name ='user.profiles'
	_description ="User Profile"
	_columns = {
		'user_profile_id' : fields.integer('User Profile ID'),
		'name':fields.char('Title', size=30, required=True),
		'sur_name':fields.char('Surname', size=20, required=True),
		'given_name':fields.char('Given Name', size=20, required=True),
		'name_nric':fields.char('Name as in NRIC', size=20, required=True),
		'user_name':fields.char('User Name', size=20, required=True),
		'password':fields.char('Password', size=20, required=True),
		'status': fields.selection((('Active','Active'),('InActive','InActive'),('Blocked','Blocked')),'Status', required=True),
		'role': fields.many2one('manage.role', 'Role', ondelete='cascade', help='Role', select=True),
		'image': fields.binary("Photo",
            help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized photo", type="binary", multi="_get_image",
            store = {
                'user.profile': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the employee. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Smal-sized photo", type="binary", multi="_get_image",
            store = {
                'user.profile': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized photo of the employee. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
		'profile_personal_tab': fields.one2many('profile.personal.details', 'personal_details_id', 'Personal Details'),
		'profile_pages_actions_tab': fields.one2many('profile.pages.actions', 'page_action_id', 'Pages & Actions'),
		'profile_notification_tab': fields.one2many('profile.notifications', 'notification_id', 'Notifications'),
		'profile_documentation_tab': fields.one2many('profile.documentations', 'documentation_id', 'Documentations'),
		'profile_history_tab': fields.one2many('profile.history', 'history_id', 'History'),
	}
users_profile()

class profile_personal_details(osv.osv):
	
	_name ='profile.personal.details'
	_description ="Personal Details"
	_columns = {
		'personal_details_id' : fields.many2one('user.profiles'),
		'name':fields.char('Items'),
	}
profile_personal_details()

class profile_pages_actions(osv.osv):
	
	_name ='profile.pages.actions'
	_description ="Pages & Actions"
	_columns = {
		'page_action_id' : fields.many2one('user.profiles'),
		'name':fields.char('Items'),
		'view':fields.boolean('View'),
		'create':fields.boolean('Create'),
		'update':fields.boolean('Update'),
	}
pages_actions()

class profile_notification(osv.osv):
	
	_name ='profile.notifications'
	_description ="Notifications"
	_columns = {
		'notification_id' : fields.many2one('user.profiles'),
		'name':fields.char('Items'),
	}
notification()

class profile_documentations(osv.osv):
	
	_name ='profile.documentations'
	_description ="Documentations"
	_columns = {
		'documentation_id' : fields.many2one('user.profiles'),
		'name':fields.char('Items'),
	}
documentations()

class profile_history(osv.osv):
	
	_name ='profile.history'
	_description ="Personal History"
	_columns = {
		'history_id' : fields.many2one('user.profiles'),
		'name':fields.char('Items'),
	}
profile_history()















