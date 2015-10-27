import datetime
from dateutil import relativedelta
from openerp import addons
import logging
import time
from lxml import etree
from collections import namedtuple
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.translate import _

import logging
import pytz
from openerp import tools
#from datetime import datetime
import re

_logger = logging.getLogger(__name__)

class client_enrollment(osv.osv):
#Total Class Calculation		
	def _calculate_total_class(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = line.client_class_tab or []
			_logger.info("total id %s",mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
		return res

# Status
	def _client_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['company_status']
		return res
		
	def _client_status_display_2(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['company_status']
		return res		
		
	def _client_status_display_3(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['company_status']
		return res		

# Unique Name Validation	
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True


# Image
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.pool.get('client.enroll').write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

# Validate Email-ID 
	def _check_unique_id(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.email_id.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.email_id and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.email_id and self_obj.email_id.lower() in  lst:
				return False
		return True

	def _check_email(self, cr, uid, ids, context=None):
		rec = self.browse(cr, uid, ids)
		cnt = 0
		for data in rec:
			xcv = data['email_id']
			if xcv:
				if len(str(xcv)) < 7:
					raise osv.except_osv(_('Warning!'),_('Email id not valid. %s') % (xcv))

				if xcv:
					for i in xcv:
						if i=='@' or i=='.':
							cnt = cnt + 1

		if xcv and cnt < 2:
			raise osv.except_osv(_('Warning!'),_('Email id not valid. %s') % (xcv))
		else:
			return True		

# Website Validate 
	def _check_unique_web(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.web_site.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.web_site and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.web_site and self_obj.web_site.lower() in  lst:
				return False
		return True
		
	def _check_web(self, cr, uid, ids, context=None):
		rec = self.browse(cr, uid, ids)
		cnt = 0
		for data in rec:
			xcv = data['web_site']
			if xcv:
				if len(str(xcv)) < 7:
					raise osv.except_osv(_('Warning!'),_('Website is not valid. %s') % (xcv))
			

				if xcv:
					for i in xcv:
						#if i=='@' or i=='.':
						if i=='.':
							cnt = cnt + 1

		if xcv and cnt < 2:
			raise osv.except_osv(_('Warning!'),_('Website is not valid. %s') % (xcv))
		else:
			return True
			
# Negative Value should not accept	
	def _postal_code(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.postal_code < 0:
				return False
		return True
		
	def _phone_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.phone_no < 0:
				return False
		return True

	def _fax_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.fax_no < 0:
				return False
		return True		

#Upload Docs
	def import_file(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(data)) 
	 # your treatment
		return		
		
# Fetching and laod in class		
	'''def load_client_class(self, cr, uid, ids, clsid, context=None):		
		val ={}
		p_obj = self.pool.get('class.info')
		value_ids = p_obj.search(cr, uid, [('client_corporate', '=', clsid)])
		#val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'class_name':prog_line['class_info'].id})
		val.update({'client_class': sub_lines})
		return {'value': val}	'''
		
# Fetching and load in class		
	'''def _load_client_class(self, cr, uid, ids, field_names, args,  context=None):
	   prog_mod_obj = self.pool.get('client.class')
	   prog_mod_ids = prog_mod_obj.search(cr, uid, [('client_corporate', '=', ids[0:])])
	   module_ids =[]
	   for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
		   if 'class_name' in prog_module_line:
			   module_ids.append(prog_module_line['class_name'].id)  
	   value_ids = self.pool.get('class.info').search(cr, uid, [('id', 'in', module_ids)])
	  # raise osv.except_osv(_('Error!'),_("client enroll %s")%(value_ids))
	   return dict([(id, value_ids ) for id in ids])

	   
# date validation in class 
	def _load_prog_client_line(self, cr, uid, ids, field_names, args,  context=None):
	   prog_mod_obj = self.pool.get('class.info')
	   prog_mod_ids = prog_mod_obj.search(cr, uid, [('class_id', '=', ids[0:])])
	   #prog_mod_ids = prog_mod_obj.search(cr, uid, [('class_id', '=', ids[0])])
	   module_ids =[]
	   for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
		   if 'start_date1' in prog_module_line:
			   module_ids.append(prog_module_line['start_date1'].id)
		   if 'start_date2' in prog_module_line:
			   module_ids.append(prog_module_line['start_date2'].id)
		   if 'start_date3' in prog_module_line:
			   module_ids.append(prog_module_line['start_date3'].id)
		   if 'start_date4' in prog_module_line:
			   module_ids.append(prog_module_line['start_date4'].id)
		   if 'start_date5' in prog_module_line:
			   module_ids.append(prog_module_line['start_date5'].id)
		   if 'start_date6' in prog_module_line:
			   module_ids.append(prog_module_line['start_date6'].id)
		   if 'start_date7' in prog_module_line:
			   module_ids.append(prog_module_line['start_date7'].id)
	   
	   value_ids = self.pool.get('client.class').search(cr, uid, [('date_end', 'in', module_ids)])
	   return dict([(id, value_ids) for id in ids])	'''
	   
	'''def client_data(self, cr, uid, ids, context=None): 
		learner_move_array = []
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		if len(learner_move_array) > 0 :
			sub_lines = []
			values = {}
			sub_lines.append( (0,0, {'class_name':self_obj['id'],'class_code':self_obj['class_code'],
				'date_start':self_obj['start_date'],'client_corporate':'name'}) )
			values.update({'client_class_tab': sub_lines})
			trainer_obj = self.pool.get("client.enroll")
			raise osv.except_osv(_('Error!'),_("Duration cannot be negative value %s")%(trainer_obj))
			for x in trainer_obj.browse(cr, uid, learner_move_array, context=context):
				trainer_obj.write(cr, uid, x.id,values, context=context)	  
		
# Fetch data from Class Calander		
	def on_change_client_class(self, cr, uid, ids, clsid):
		val={}
		obj = self.pool.get('class.info')
		ids = obj.search(cr, uid, [('class_id','=',clsid)])
		records = obj.browse(cr, uid, ids)		
		sub_lines = []
		for prog_line in obj.browse(cr, uid, ids):
			sub_lines.append({'class_name':prog_line['class_info'].id})
			val.update({'client_class_tab': sub_lines})
		return {'value': val}''' 
		
		
	_name = "client.enroll"
	_description = "This table is for keeping Client data"
	_columns = {
		'client_id': fields.char('Id',size=10),
		'parent_id': fields.integer('Parent Id',size=20),
		'name': fields.char('Company Name', size=40, required=True, help='Name of the Company'),
		'company_status': fields.selection((('Active','Active'),('InActive','InActive'),('Complete','Complete'),('InComplete','InComplete'),('Blocked','Blocked')),'Status', required=True),
		'client_status_display_1': fields.function(_client_status_display_1, readonly=1, type='char'),
		'client_status_display_2': fields.function(_client_status_display_2, readonly=1, type='char'),
		'client_status_display_3': fields.function(_client_status_display_3, readonly=1, type='char'),
		'date1': fields.date('Date Created', readonly='True'),
		'date2': fields.date('Date Created', readonly='True'),
		'address_1': fields.text('Address'),
		'postal_code': fields.integer('Postal', size=7),
		'phone_no': fields.integer('Phone', size=9),
		'fax_no': fields.integer('Fax', size=9),
		'email_id': fields.char('Email', size=30),
		'web_site': fields.char('Website', size=30),
		'image': fields.binary("Photo",
			help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
			string="Medium-sized photo", type="binary", multi="_get_image",
			store = {
				'client.enroll': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Medium-sized photo of the employee. It is automatically "\
				 "resized as a 128x128px image, with aspect ratio preserved. "\
				 "Use this field in form views or some kanban views."),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
			string="Smal-sized photo", type="binary", multi="_get_image",
			store = {
				'client.enroll': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Small-sized photo of the employee. It is automatically "\
				 "resized as a 64x64px image, with aspect ratio preserved. "\
				 "Use this field anywhere a small image is required."), 
				 
		'contact_tab': fields.one2many('contact.info','contact_id','Contacts'),				
		#'client_class_tab': fields.function(_load_prog_client_line, relation='client.class',readonly=1,type='one2many', string='Class'),		 
		'client_class_tab': fields.one2many('client.class','class_id','Client Class'), 
		'client_learner_tab': fields.one2many('client.learner','learner_id','Client Learner'),	
		'upld_resume': fields.binary('Upload Documents'),
		'datas_fname': fields.char('File Name'),	
		'client_history_tab': fields.one2many('client.history','history_id1','Client history'),	
		# Finance Tab
		'client_finance_tab': fields.one2many('client.finance','finance_id','Client Finance', help='details about Finance'),	
		'credit_term':fields.char('Credit Term'),
		'credit_limit':fields.char('Credit Limit'),
		'pre_pay_mod':fields.many2one('master_pay.mod','Preferred Payment Method'),
		'key_person':fields.many2one('keyperson', 'Key Person'),
		# EOF
		'actual_number':fields.function(_calculate_total_class, relation="client.enroll",readonly=1,string='No. Classes',type='integer'),
	}

	_defaults = { 
	   'date1': fields.date.context_today,
	   'date2': fields.date.context_today,
	   'company_status': 'Active',
	}	
	
	
	_constraints = [(_check_email, 'Error! Email is invalid.', ['work_email']),(_check_unique_id, 'Error: Email Already Exist', ['Email']),
	(_check_web, 'Error: Website is invalid', ['Website']),(_check_unique_web, 'Error: Website Already Exist', ['Website']),
	(_postal_code, 'Error: Postal Code Cannot be Negative', ['Postal']),(_phone_no, 'Error: Phone Number Cannot be Negative', ['Phone']),
	(_fax_no, 'Error: Fax Number Cannot be Negative', ['Fax']),(_check_unique_name, 'Error: Company Name Already Exist', ['Name'])]		
client_enrollment()

class contact_info(osv.osv):

# Validate Email-ID 
	def _check_unique_id1(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.email_id_1.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.email_id_1 and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.email_id_1 and self_obj.email_id_1.lower() in  lst:
				return False
		return True

	def _check_email2(self, cr, uid, ids, context=None):
		rec = self.browse(cr, uid, ids)
		cnt = 0
		for data in rec:
			xcv = data['email_id_1']
			if xcv:
				if len(str(xcv)) < 7:
					raise osv.except_osv(_('Warning!'),_('Email id not valid. %s') % (xcv))

				if xcv:
					for i in xcv:
						if i=='@' or i=='.':
							cnt = cnt + 1

		if xcv and cnt < 2:
			raise osv.except_osv(_('Warning!'),_('Email id not valid. %s') % (xcv))
		else:
			return True	


# Negative Value should not accept			
	def _ph_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.ph_no < 0:
				return False
		return True

	def _mobile_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.mobile_no < 0:
				return False
		return True

	def _extn_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.extn_no < 0:
				return False
		return True	


#Unique Moblie, Extn and Ph no.		
	def _check_unique_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mobile_no == self_obj.mobile_no and x.contact_id == self_obj.contact_id:
						return False
		return True

	def _check_extn_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.extn_no == self_obj.extn_no and x.contact_id == self_obj.contact_id:
						return False
		return True

	def _check_phn_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.ph_no == self_obj.ph_no and x.contact_id == self_obj.contact_id:
						return False
		return True		
		
# Unique Contact Name		
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True		
	
	_name = "contact.info"
	_description = "Contact info"
	_columns = {
	'contact_id' : fields.integer('Id', readonly='True'),
	'name': fields.char('Name', size=30, required=True),
	'position': fields.char('Position', size=20),
	'email_id_1': fields.char('Email'),
	'ph_no': fields.integer('Phone', size=9),
	'extn_no': fields.integer('Extn', size=9),
	'mobile_no': fields.integer('Mobile', size=9),
	'Alt_addr': fields.text('Alternate Address'),
	'main_contact': fields.boolean('Main Contact'),
	}	

	_constraints = [(_check_extn_no, 'Error! EXTN No. Already Exist.', ['Extn']),(_check_phn_no, 'Error! Phone No. Already Exist.', ['Phone']),(_check_unique_no, 'Error! Mobile No. Already Exist.', ['Mobile']),(_check_unique_name, 'Error! Contact Name Already Exist.', ['Name']),(_check_email2, 'Error! Email Id is Invalid.', ['Email']),(_check_unique_id1, 'Error: Email Already Exist', ['Email']),(_mobile_no, 'Error: Mobile Number Cannot be Negative', ['Mobile']), (_ph_no, 'Error: Phone Number Cannot be Negative', ['Phone']), (_extn_no, 'Error: Extn Number Cannot be Negative', ['Extn']),]
	
	_defaults={
	'main_contact': True
	} 
contact_info()

# Class Tab
class client_class(osv.osv):


	'''def on_change_client_class(self, cr, uid,id, ids, i_centre):
		val ={}
		sub_lines = []
		val.update({'class_name': ''})
		val.update({'class_code': ''})
		val.update({'Client_status': ''})
		val.update({'date_start': ''})
		val.update({'date_end': ''})
		#val.update({'class_name': i[0]})
		val.update({'client_class_tab': sub_lines})

		if i_centre:
			sql="select distinct class_name from client_class where class_id = %s" % (i_centre)
			#sql="select module_id from select_module where id = %s" % (i_mod)
			cr.execute(sql)
			r = cr.fetchall()
			for i in r:
				if i[0]:
					val.update({'class_name': i[0]})

		return  {'value': val}'''
		
	'''def _create_client(self, cr, uid, ed, sd, mn, cc, values, context=None):
			obj_res_hist = self.pool.get('client.class')
			
			for ch in values:
				#raise osv.except_osv(_('Error!'),_("Duration cannot be client negative value %s ")%(ch['class_id']))
				sql="select distinct class_name from client_class where class_id = %s" % (cn['class_id'],)
				cr.execute(sql)
				itm = cr.fetchall()
				for s in itm:
					cn = s[0]
					cc = s[1]
					dd = s[2]
					ss = s[3]
					es = s[4]
					
				#raise osv.except_osv(_('Error!'),_("Duration cannot be negative value %s %s %s %s")%(ed,
				#obj_li=self.pool.get('learner.info').browse(cr, uid, ch['learner_id'])

				vals = {
					'class_name': cn['class_id'],
					'class_code': cc,
					'Client_status': dd,
					'date_start': ss,
					'end_date':ed,
				#	'class_id':ch['learner_id'],
				#	'class_code':cc,
				#	'start_date': sd,
				#	'module_name':mn
				}
				obj_res_hist.create(cr, uid, vals, context=context)
			return True	'''
	'''def confirm_broadcast(self, cr, uid, ids, context=None): 
		learner_move_array = []
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		class_obj = self_obj['class_name']
		for le_obj in class_obj.client_corporate:
			_logger.info("TrainerLineId %s",le_obj.id)
			if le_obj.trainer_id.id == self_obj.class_id :
				_logger.info("TrainerLineId %s",le_obj.id)
		#		self.pool.get("trainers.line").update_status(cr, uid, le_obj.id,{'t_status':'Accepted'}, context=context)
				self.pool.get("class.info").update_status(cr, uid, le_obj.id,{'company_status':'Active'}, context=context)
		super(avaliable, self).write(cr, uid, ids[0],{'status':'In Progress'}, context=context)	
		return True		'''
	#	super(client_class, self).write(cr, uid, ids[0], context=context)	
	
	#def update_status(self,cr, uid, ids, values, context=None):
	#	super(client_class, self).write(cr, uid, ids,values, context=context)	
	#	for er in trainers:
	#		self.pool.get('client.class').update_status(cr, uid, er,{'t_status':'Awaiting Response'}, context=context)


		
	_name = "client.class"
	_description = "Client class"
	_columns = {
	'class_id' : fields.integer('Id', readonly='True'),
	#'parent_id' : fields.integer('Id', readonly='True'),
	'client_corporate': fields.many2one('client.enroll','Corporate', ondelete='cascade', help='Client', select=True),
	'class_name': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True, required=True),
	'parent_id': fields.related('class_name','parent_id',type="integer",relation="class.enroll",string="Parent Id", readonly=1, required=True),
	'class_code': fields.related('class_name','class_code',type="char",relation="class.info",string="Class Code", readonly=1),	
# Status is Hardcoded in Class Calender
	#'Client_status': fields.related('class_name','status',type="char",relation="class.info",string="Status", readonly=1),
	#'Client_status': fields.selection((('Complete','Complete'),('InComplete','InComplete'),('In Progress','In Progress')),'Status', required=True),
	'Client_status': fields.char('Status', readonly=1),
	'date_start': fields.related('class_name','start_date',type="date",relation="class.info",string="Date Start", readonly=1),
	'date_end': fields.related('class_name','end_date',type="date",relation="class.info",string="Date End", readonly=1),
	'pax_no': fields.related('class_name','no_of_learners',type="integer",relation="class.info",string="Pax", readonly=1),
	
	}
	
	_defaults = { 
	   'Client_status': 'In Progress',
	}	
	
client_class()


# Learner Tab
class client_learner(osv.osv):

# Unique NRIC Validation
	def _check_unique_learner_nric(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.learner_nric.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.learner_nric and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.learner_nric and self_obj.learner_nric.lower() in  lst:
				return False
		return True

	_name = "client.learner"
	_description = "Client Learner"
	_columns = {
	'learner_id' : fields.integer('Id', readonly='True'),
	'client_corporate': fields.many2one('client.enroll','Corporate', ondelete='cascade', help='Client', select=True),
	'learner_name':fields.char('Name',size=20,required=True),
	'learner_nric':fields.char('NRIC',required=True),	
	'class_name_1': fields.many2one('class.info','Class', ondelete='cascade', help='Class', select=True, required=True),
	'class_code_1': fields.related('class_name_1','class_code',type="char",relation="class.info",string="Class Code", readonly=1),
	'Client_status_1': fields.selection((('Complete','Complete'),('InComplete','InComplete'),('In Progress','In Progress')),'Status'),
	#'Client_status_1': fields.related('class_name_1','status',type="char",relation="class.info",string="Status", readonly=1),
	'date_start_1': fields.related('class_name_1','start_date',type="date",relation="class.info",string="Date Start", readonly=1),
	'date_end_1': fields.related('class_name_1','end_date',type="date",relation="class.info",string="Date End", readonly=1),
	}	
	
	_defaults = { 
	   'Client_status_1': 'In Progress',
	}	
	
	_constraints = [(_check_unique_learner_nric, 'Error: NRIC Already Exists', ['NRIC'])]
	
client_learner()


class master_learner(osv.osv):
	
	_name ='master.learner'
	_description ="master learner Tab"
	_columns = {
	'name':fields.char('Name',size=20,required=True),
	'nric':fields.char('NRIC',required=True),	
	}
master_learner()	

# Finance Tab with its Master Tab
class client_finance(osv.osv):
	
	_name = "client.finance"
	_description = "Client Learner"
	_columns = {
	'finance_id' : fields.integer('Id', readonly='True'),
	}	
client_finance()

class master_key_person(osv.osv):
	
	_name = "keyperson"
	_description = "Master Key Person"
	_columns = {
	'key_id' : fields.integer('Id', readonly='True'),
	}	
master_key_person()

class master_pre_pay_mod(osv.osv):
	
	_name = "master_pay.mod"
	_description = "Master Pre Payment Module"
	_columns = {
	'key_id' : fields.integer('Id', readonly='True'),
	}	
master_pre_pay_mod()
# EOF Finance

# History Tab
class client_history(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(client_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name ="client.history"
	_description ="History Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=3,readonly=1),
	'history_id1':fields.integer('Id',size=3),
	'date_created':fields.date('Date Created'),
	'created_by':fields.char('Created By',size=20),
	'last_update':fields.char('Last Update',size=20),
	'last_update_by':fields.char('Last Update By',size=20),
	'date_status_change':fields.char('Date Of Status Change',size=20),
	'status_change_by':fields.char('Status Change By',size=20),
	'changes':fields.char('Changes',size=20),
	'test_id': fields.many2one('test', 'Test', ondelete='cascade', help='Test', select=True),
	}
	
client_history()


	