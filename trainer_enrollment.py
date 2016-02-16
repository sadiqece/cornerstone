from dateutil import relativedelta
from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from datetime import datetime, timedelta, date
import re

_logger = logging.getLogger(__name__)

####################
#TRAINER PROFILE PAGE
####################

#Trainer
###############

class trainer_profile_info(osv.osv):

# Trainer Unique Name
	def _check_unique_trainer_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
		
# Trainer NAME/NRIC Unique Name		
	def _check_unique_name_nric_fin(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.nric_name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.nric_name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.nric_name and self_obj.nric_name.lower() in  lst:
				return False
		return True

# Trainer NAME/NRIC Unique Name		
	def _check_unique_nric_fin(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.nric.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.nric and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.nric and self_obj.nric.lower() in  lst:
				return False
		return True
		
#Module Status
	def _trainer_status_display(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['trainers_status']
		return res

	def _trainer_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['trainers_status']
		return res
			
# Validate Email-id			
	def ValidateEmail(self, cr, uid, ids, email_id):
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_id) != None:
			return True
		else:
			raise osv.except_osv('Invalid Email', 'Please enter a valid email address')
			
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

# Uploading Images		
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
# Validation for negative values
	def _mobile_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.mobile_no < 0:
				return False
		return True

# Validation for negative values		
	def _landline_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.landline_no < 0:
				return False
		return True

# Validation for negative values		
	def _office_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.office_no < 0:
				return False
		return True

# Validation for negative values		
	def _no_children(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.No_of_Children < 0:
				return False
		return True

# Validate Email		
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
	
	def _ass_func_1(self, cr, uid, ids, expenses, arg, context):
		value_ids = self.pool.get('trainers.assignment.avaliable').search(cr, uid, [])
		return_ids = []
		for x in self.pool.get('trainers.assignment.avaliable').browse(cr,uid,value_ids) :
			if datetime.today().date() < datetime.strptime(x.start_date_avaliable,"%Y-%m-%d %H:%M:%S").date():
				return_ids.append(x.id)
		return dict([(id, return_ids ) for id in ids])
	
	def _ass_func_2(self, cr, uid, ids, expenses, arg,  context):
		value_ids = self.pool.get('trainers.assignment.avaliable').search(cr, uid, [])
		return_ids = []
		for x in self.pool.get('trainers.assignment.avaliable').browse(cr,uid,value_ids) :
			if datetime.today().date() > datetime.strptime(x.start_date_avaliable,"%Y-%m-%d %H:%M:%S").date():
				return_ids.append(x.id)
		return dict([(id, return_ids ) for id in ids])
		
	def copy(self, cr, uid, id, default=None, context=None):
		group_name = self.read(cr, uid, [id], ['name'])[0]['name']
		group_name_one = self.read(cr, uid, [id], ['nric_name'])[0]['nric_name']
		group_name_two = self.read(cr, uid, [id], ['nric_name'])[0]['nric_name']
		default.update({'name': _('%s (copy)')%group_name})
		default.update({'nric_name': _('%s (copy)')%group_name_one})
		default.update({'nric': _('%s (copy)')%group_name_two})
		return super(trainer_profile_info, self).copy(cr, uid, id, default, context)
		
#Table For Trianer Profile 'trainer_profile_info'			
	_name = "trainer.profile.info"
	_description = "This table is for keeping location data"
	_columns = {
	'location_id': fields.integer('Id',size=20),
	'name': fields.char('Name:', size=100,required=True, select=True),
	'image': fields.binary("Image"),
	'nric_name': fields.char('Name as in NRIC/FIN:', size=100,required=True),
	'nric': fields.char('NRIC/FIN:', size=12,required=True),
	'trainers_status': fields.selection((('Active','Active'),('InActive','InActive')),'Status', required=True, select=True),
	'date1': fields.date('Date Created', readonly='True'),
	'date2': fields.date('Date Created', readonly='True'),
	'trainer_id': fields.many2one('panel.info','Trainer',ondelete='cascade', help='Class Calendar', select=True),
	'trainer_status_display': fields.function(_trainer_status_display, readonly=1, type='char'),
	'trainer_status_display_1': fields.function(_trainer_status_display_1, readonly=1, type='char'),
	'assignment_avaliable': fields.one2many('trainers.assignment.avaliable','trainer_avail_id','Available', readonly=1),
	'assignment_current': fields.function(_ass_func_1,type='one2many',obj="trainers.assignment.avaliable",method=True,string='Session'),
	'assignment_history': fields.function(_ass_func_2,type='one2many',obj="trainers.assignment.avaliable",method=True,string='Session'),
	'trainer_module_line': fields.one2many('trainer.module.line','trainers_id','Module',),
	'trainer_modules_category': fields.one2many('trainer.module.category','trainers_category_id','Category'),
	'non_avaliable': fields.one2many('non.availability','s_no','Non-Avaliablity'),
	#'personal_line': fields.one2many('personal.detail.module','personal_detail_id','Personal Details'),
	'nationality':fields.selection((('Singapore','Singapore'),('Malaysia','Malaysia'),('South Korea','South Korea'),('North Korea','North Korea'),('India','India'),('Indonesia','Indonesia'),('Vietnam','Vietnam')),'Nationality'),
	'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
	'trainer_category': fields.selection((('Key','Key'),('Core','Core'),('Standard','Standard')),'Trainer Category'),
	'race':fields.many2one('race', 'Race'),
	'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
	'Religion': fields.char('Religion', size=10),
	'No_of_Children':fields.integer('No of Children', size=2),
	'email_id': fields.char('Email', size=30),
	'addr_1': fields.char('Address Line 1'),
	'addr_2': fields.char('Address Line 2'),
	'postal_code': fields.char('Postal Code', size=6),
	'mobile_no': fields.integer('Mobile', size=9),
	'landline_no': fields.integer('Home', size=9),
	'office_no': fields.integer('Office', size=9),
	'qualification_line': fields.one2many('qualification.trainer.module','qualify_id','Qualification'),
	'work_exp_line': fields.one2many('work.exp.module','work_id','Work Experience',),
	'image': fields.binary("Photo",
				help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
			'image_medium': fields.function(_get_image, fnct_inv=_set_image,
				string="Medium-sized photo", type="binary", multi="_get_image",
				store = {
					'trainer.profile.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
				},
				help="Medium-sized photo of the employee. It is automatically "\
					"resized as a 128x128px image, with aspect ratio preserved. "\
					"Use this field in form views or some kanban views."),
			'image_small': fields.function(_get_image, fnct_inv=_set_image,
				string="Smal-sized photo", type="binary", multi="_get_image",
				store = {
					'trainer.profile.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
				},
				help="Small-sized photo of the employee. It is automatically "\
					"resized as a 64x64px image, with aspect ratio preserved. "\
					"Use this field anywhere a small image is required."),
	}
	_defaults = { 
	   'date1': fields.date.context_today,
	   'date2': fields.date.context_today,
	   'trainers_status': 'Active',
	   'nationality': 'Singapore',
    }
	_constraints = [(_check_unique_trainer_name, 'Error: Trainer Already Exists', ['Trainer Name']),(_check_unique_name_nric_fin, 'Error: Trainer NRIC/FIN Already Exists', ['NRIC/FIN']),(_check_unique_nric_fin, 'Error: Trainer NRIC/FIN Already Exists', ['NRIC/FIN']),(_check_unique_id, 'Error: Email Already Exist', ['Email']),(_mobile_no, 'Error: Mobile Number Cannot be Negative', ['Mobile']), (_landline_no, 'Error: Landline Number Cannot be Negative', ['Landline']), (_office_no, 'Error: Office Number Cannot be Negative', ['Office']), (_no_children, 'Error: Number of childrens Cannot be Negative', ['Children']), (_check_email, 'Error! Email is invalid.', ['work_email'])]
trainer_profile_info()

# Assignment Tab
class avaliable(osv.osv):
	def confirm_broadcast(self, cr, uid, ids, context=None): 
		learner_move_array = []
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		class_obj = self_obj['class']
		for le_obj in class_obj.trainers_line:
			_logger.info("TrainerLineId %s",le_obj.id)
			if le_obj.trainer_id.id == self_obj.trainer_avail_id :
				_logger.info("TrainerLineId %s",le_obj.id)
				self.pool.get("trainers.line").update_status(cr, uid, le_obj.id,{'t_status':'Accepted'}, context=context)
		super(avaliable, self).write(cr, uid, ids[0],{'status':'Accepted'}, context=context)

	def decline_broadcast(self, cr, uid, ids, context=None): 
		learner_move_array = []
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		class_obj = self_obj['class']
		for le_obj in class_obj.trainers_line:
			if le_obj.trainer_id.id == self_obj.trainer_avail_id :
				self.pool.get("trainers.line").update_status(cr, uid, le_obj.id,{'t_status':'Declined'}, context=context)
		super(avaliable, self).write(cr, uid, ids[0],{'status':'Declined'}, context=context)
	
	_name ='trainers.assignment.avaliable'
	_description ="Assignment Available Tab"
	_columns = {
	'trainer_avail_id' : fields.integer('Trainer_Avail_Id',size=20,readonly=1),
	'class': fields.many2one('class.info', 'Class', ondelete='cascade', help='Module', select=True),
	'class_code_avaliable': fields.related('class','class_code',type="char",relation="class.info",string="Class Code"),
	'start_date_avaliable': fields.related('class','start_date',type="datetime",relation="class.info",string="Start Date"),
	'status':fields.char('Status',size=10),
	}
avaliable	()

# Module Tab
class trainer_module_category(osv.osv):

	_name = "trainer.module.category"
	_description = "Module Category Tab"
	_columns = {
	'trainers_category_id' : fields.many2one('trainer.profile.info', 'Module'), 
	'category':fields.many2one('master.category', 'Category', ondelete='cascade', help='Category', select=True, required=True),
	'selected_date':fields.date('Selected'),
	}
trainer_module_category()

class master_category(osv.osv):
	
	_name = "master.category"
	_description = "Master Category Tab"
	_columns = {
		'name': fields.char('Category', size=25)
	}
master_category()

# Module Tab
class trainer_module(osv.osv):

	def _check_unique_module_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.trainers_id == self_obj.trainers_id and x.trainer_module_id == self_obj.trainer_module_id:
						return False
		return True
		
#dob
	def months_between(self, date1, date2):
		date11 = datetime.now.datetime.now.strptime(date1, '%Y-%m-%d')
		date12 = datetime.now.datetime.now.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
	
	def onchange_dob(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.now.datetime.now().date()))
			res = {'value':{}}
			if d < 0:
				res['value']['trainer_date'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, future date not allowed.')}})
				return res
			return dob
		
	def _trainer_rate(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.trainer_rate < 0:
				return False
		return True

	_name = "trainer.module.line"
	_description = "Module Tab"
	_columns = {
	'trainers_id' : fields.many2one('trainer.profile.info', 'Module'), 
	'trainer_module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
	'trainer_code': fields.related('trainer_module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
	'trainer_rate': fields.integer('Trainer Rate', size=6),
	'category':fields.many2one('master.category', 'Category', ondelete='cascade', help='Category', select=True, required=True),
	'core': fields.boolean('Core'),
	'key': fields.boolean('Key'),
	'support': fields.boolean('Support'),
	'trainer_mod_status': fields.selection((('Active','Active'),('Pending','Pending')),'Status', required=True),
	'trainer_date':fields.date('Date', required=True),
	}
	
	_defaults = {
	   'trainer_date': fields.date.context_today,
	}
	
	_constraints = [(_check_unique_module_name, 'Error: Module Already Exists', ['Module Name']), (_trainer_rate, 'Error: Trainer Rate Cannot be Negative', ['Trainer Rate'])]
trainer_module()

#Non-Avaliablity
class non_avaliablity(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(non_avaliablity, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
#Validate Unique Start Date
	def _check_unique_start_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.s_no == self_obj.s_no and x.start_date == self_obj.start_date:
						raise osv.except_osv(_('Error:'),_('Start Date Already Exists')%(self_obj))
		return True
		
#Validate Unique End Date
	def _check_unique_end_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.s_no == self_obj.s_no and x.end_date == self_obj.end_date:
						raise osv.except_osv(_('Error:'),_('End Date Already Exists')%(self_obj))
		return True
		
	def _get_days(self, cr, uid, ids, field_name, arg ,context=None):
		res = {}
		fmt = '%Y-%m-%d'
		for object in self.browse(cr, uid, ids, context=context):
			res[object.id] = {'total_days':0, } 
			from_date = object.start_date 
			to_date = object.end_date
			d1 = datetime.strptime(from_date, fmt)
			d2 = datetime.strptime(to_date, fmt)
			daysDiff = str((d2-d1).days+1)
			res[object.id]['total_days'] = daysDiff
			return res
	
	_name = "non.availability"
	_description = "Non Availability"
	_columns = {
		's_no' : fields.integer('S.No',size=20,readonly=1),
		'start_date': fields.date('Start Date', required=True),
		'end_date': fields.date('End Date', required=True),
		'total_days': fields.function(_get_days, string="Diff days", multi='sums', store=True),
		'half_day': fields.boolean('1/2 Day'),
		'am_pm': fields.selection((('AM','AM'),('PM','PM'),('Empty','Empty')), 'am/pm')
	}
	_constraints = [(_check_unique_start_date, 'Error: Start Date Already Exists', ['Start Date']),(_check_unique_end_date, 'Error: End Date Already Exists', ['End Date'])]
non_avaliablity()

# Personal Details Tab
class personal_detail(osv.osv):
	_name = "personal.detail.module"
	_description = "Personal Details Tab"
	_columns = {
	'personal_detail_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
personal_detail()

class master_race(osv.osv):
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
	_name ='race'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Race',size=10),
	}
	_constraints = [(_check_unique_race, 'Error: Race Already Exists', ['Race'])]
master_race()

# Qualification Tab
class qualification(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(qualification, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _check_unique_certification(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.qualify_id == self_obj.qualify_id and x.certification == self_obj.certification:
						return False
		return True
		
	_name = "qualification.trainer.module"
	_description = "Qualification Tab"
	_columns = { 
	'qualify_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,),		
	'certification':fields.char('Certification',size=25),
	'institution':fields.char('Institution',size=25),
	'board_university':fields.char('Board/University',size=25),
	'year_awarded':fields.selection([(num, str(num)) for num in range(1900, (datetime.now().year)+1 )], 'Year Awarded'),
	'Prof_Cert': fields.boolean('Prof Cert'),
	}
	_constraints = [(_check_unique_certification, 'Error: Certification Already Exists', ['Certification'])]
qualification()

# Work Expressions Tab
class work_exp(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(work_exp, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _year_from_to(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.year_to < self_obj.year_from:
				return False
		return True
		
	def _year_from_from_one(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.work_id == self_obj.work_id and self_obj.year_from < x.year_from:
						return False
		return True
		
	def _check_unique_year_from(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.work_id == self_obj.work_id and x.year_from == self_obj.year_from:
						return False
		return True
		
	def _check_unique_year_to(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.work_id == self_obj.work_id and x.year_to == self_obj.year_to:
						return False
		return True
		
	def _check_all_range(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, uid ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.work_id == self_obj.work_id and x.year_to == self_obj.year_to and x.year_from == self_obj.year_from:
						return False
					elif x.work_id == self_obj.work_id and self_obj.year_from > x.year_from and self_obj.year_from < x.year_to:
						return False
					elif x.work_id == self_obj.work_id and self_obj.year_to > x.year_from and self_obj.year_to < x.year_to:
						return False
		return True
		
	def import_file(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(data)) 
	 # your treatment
		return

	_name = "work.exp.module"
	_description = "Work Experience Tab"
	_columns = {
	'work_id' : fields.many2one('trainer.profile.info', 'Work Experience', ondelete='cascade', help='Trainer Profile', select=True, readonly=1),
	's_no' : fields.integer('S.No',size=20,readonly=1),	
	'company':fields.char('Company',size=25, required=True),
	'industry':fields.char('Industry',size=25),
	'position':fields.char('Position',size=25),
	'year_from':fields.selection([(num, str(num)) for num in range(1900, (datetime.now().year)+1 )], 'Year From', required=True),
	'year_to': fields.selection([(num, str(num)) for num in range(1900, (datetime.now().year)+1 )], 'Year To', required=True),
	'key_responsibility':fields.char('Key Responsibilities'),
	'trg_specific':fields.boolean('Trg Specific'),
	'upl_resume': fields.binary('Upload Documents'),
	'datas_fname': fields.char('File Name'),
	'file_type': fields.char('Content Type'),
	'index_content': fields.text('Indexed Content'),
	}
	_constraints = [(_year_from_to, 'Error: Year To should be greater than Year From', ['Year']), (_check_unique_year_from, 'Error: Year From Already Exists', ['Year From']), (_check_unique_year_to, 'Error: Year To Already Exists', ['Year To']), (_check_all_range, 'Error: Years already Exists', ['Check Years']), (_year_from_from_one, 'Error: Year From should not be less than Pervious Year', ['Check Years'])]
work_exp()

# Invoice Tab
class invoice(osv.osv):
	_name = "invoice.module"
	_description = "invoice Tab"
	_columns = {
	'invoice_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
invoice()

####################
#EOF Trainer Profile 
####################

####################
#Assignment Schedule and Settings
####################

#Assignment Schedule
###############

class panel_info(osv.osv):

	_name = "panel.info"
	_description = "This table is for keeping location data"
	_columns = {
	'trainer_line': fields.one2many('trainer.line','trainer_id','Trainers',ondelete='cascade', help='Class Calendar', select=True),
	'asssign_schedule_line': fields.one2many('assign.schedule.line','sche_id','Assignment Schedules'),
	'assigned_line': fields.one2many('assignment.schedule','assigned_id','Assignment Schedule',ondelete='cascade', help='Class Calendar', select=True),
	'trainer_ids' : fields.one2many('trainer.profile.info', 'trainer_id', 'Trainer', ondelete='cascade', help='Class Calendar', select=True),
	'name': fields.related('trainer_ids','name', string='Status', type="char", relation="trainer.profile.info", readonly=1),
	'all_trainer':fields.many2one('trainer.profile.info', 'All Trainer',ondelete='cascade', help='Program', select=True),
	'class_sched':fields.many2one('class.info','Class',ondelete='cascade', help='Program', select=True),
	'start_date':fields.related('class_sched','start_date', string='Date', type="char", relation="class.info", readonly=1),
	'mod_sched':fields.many2one('cs.module','Module',ondelete='cascade', help='Program', select=True),
	'scheduled_date': fields.char('Scheduled Date'),
	}
	
#Trainer Schedule Details	
	def onchange_trainer_hist(self, cr, uid, ids, i_trainer, i_class, context=None):
		val ={}
		sub_lines = []
		#raise osv.except_osv(_('Warning!'),_('Email id not valid. %s %s %s') % (i_trainer, i_class, i_mod))
		val.update({'assigned_line':''})
		if i_trainer:
			sql  ="select distinct c.name, c.module_id, c.start_date from class_info c, cs_module cs, trainers_line t, trainer_profile_info tp where c.module_id = cs.id and c.id = t.trainers_line_id and t.trainer_id = tp.id and tp.id = %s" % (i_trainer)
			cr.execute(sql)
			itm = cr.fetchall()
			
			for s in itm:
				sub_lines.append({'name': s[0], 'mod_sched': s[1], 'scheduled_date': s[2]})
					
				val.update({'assigned_line': sub_lines})
			
			return {'value': val}
		else:
			return val
panel_info()

class assignment_schedule(osv.osv):
	_name = "assignment.schedule"
	_description = "Assignment Schedule"
	_columns = {
		'assigned_id': fields.many2one('panel.info','ID',ondelete='cascade', help='Class Calendar', readonly=1),
		'name': fields.char('Class Name', size=20, readonly=1),
		'mod_sched' : fields.many2one('cs.module', 'Module Name', size=20, readonly=1),
		'scheduled_date': fields.date('Scheduled Date', readonly=1),
	}
assignment_schedule()

#Settings
###############

class setting_panel(osv.osv):

	def _class_start_notice(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.class_start_notice < 0:
				return False
		return True
		
	def _class_outstanding_notice(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.class_outstanding_noitce < 0:
				return False
		return True
		
	def _trainer_min_avail(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.trainer_min_avail < 0:
				return False
		return True
		
	def _base_rate(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.base_rate < 0:
				return False
		return True

	_name = "setting.line"
	_description = "Settings"
	_columns = {
	'class_start_notice': fields.integer('Class Start Notice', size=5),
	'class_outstanding_noitce': fields.integer('Class Outstanding Notice', size=5),
	'trainer_min_avail': fields.integer('Trainer Min Avaliablity (%)', size=5),
	'base_rate': fields.integer('Base Rate ($ per hr)', size=4),
	}
	_constraints = [(_class_start_notice, 'Error: Class Start Notice Cannot be Negative', ['Start Notice']),(_class_outstanding_notice, 'Error: Class Outstanding Notice Cannot be Negative', ['Outstanding Notice']),(_trainer_min_avail, 'Error: Trainer Min Avaliablity (%) Cannot be Negative', ['Avaliablity']),(_base_rate, 'Error: Base Rate ($ per hr) Cannot be Negative', ['Base Rate'])]
setting_panel()
