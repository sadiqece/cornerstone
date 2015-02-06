from dateutil import relativedelta
from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from datetime import datetime
import re

_logger = logging.getLogger(__name__)

class edu_info(osv.osv):
	_name = "edu.info"
	_description = "This table is for keeping location data"
	_columns = {
	'assign_line': fields.one2many('assign.module.line','assign_id','Assignment Required'),
	'assign_confirm': fields.one2many('confirm.module.line','assign_id','Assignment Confirmation'), 
	'assign_outstanding': fields.one2many('outstanding.module.line','assign_id','Assignment Outstanding'),
	}
edu_info()

class assignment_req(osv.osv):
	_name = "assign.module.line"
	_description = "This table is for keeping assignment data"
	_columns = {
	'assign_id' : fields.integer('Id',size=20), 
	'class_name': fields.char('Class', size=100),
	'class_code': fields.char('Class Code', size=100),
	'location_name': fields.char('Location', size=100),
	'date_start': fields.date('Date Start'),
	'date_schesule': fields.date('Date Schedule'),
	'days_left': fields.char('Days Left', size=50),
	
	}	
assignment_req ()


class assignment_confirm(osv.osv):
	_name = "confirm.module.line"
	_description = "This table is for keeping assignment confirmation data"
	_columns = {
	'assign_id' : fields.integer('Id',size=20), 
	'class_name': fields.char('Class', size=100),
	'class_code': fields.char('Class Code', size=100),
	'location_name': fields.char('Location', size=100),
	'assign_date': fields.date('Assignment Date'),
	'no_assign': fields.date('No assigned'),
	'no_of_resp': fields.char('No of Responses'),
	'date_start': fields.date('Date Start'),
	'date_schesule': fields.date('Date Schedule'),
	'days_left': fields.char('Days Left', size=50),
	
	}	
assignment_confirm ()

class assignment_outstanding(osv.osv):
	_name = "outstanding.module.line"
	_description = "This table is for keeping assignment outstanding data"
	_columns = {
	'assign_id' : fields.integer('Id',size=20), 
	'class_name': fields.char('Class', size=100),
	'class_code': fields.char('Class Code', size=100),
	'location_name': fields.char('Location', size=100),
	'assign_date': fields.date('Assignment Date'),
	'no_assign': fields.date('No assigned'),
	'no_of_resp': fields.char('No of Responses'),
	'date_start': fields.date('Date Start'),
	'date_schesule': fields.date('Date Schedule'),
	'days_left': fields.char('Days left', size=50),
	
	}	
assignment_outstanding ()


class panel_info(osv.osv):

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

	_name = "panel.info"
	_description = "This table is for keeping location data"
	_columns = {
	'trainer_line': fields.one2many('trainer.line','trainer_id','Trainers'),
	'asssign_schedule_line': fields.one2many('assign.schedule.line','sche_id','Assignment Schedules'),
	'assigned_line': fields.one2many('assignment.schedule','assigned_id','Assignment Schedule',ondelete='cascade', help='Class Calendar', select=True),
	'setting_panel_line': fields.one2many('setting.line','setting_id','Settings'),
	'class_start_notice': fields.integer('Class Start Notice', size=6),
	'class_outstanding_noitce': fields.integer('Class Outstanding Notice', size=6),
	'trainer_min_avail': fields.integer('Trainer Min Avaliablity (%)', size=6),
	'base_rate': fields.integer('Base Rate ($ per hr)', size=4),
	'trainer_ids' : fields.one2many('trainer.profile.info', 'trainer_id', 'Trainer'),
	'name': fields.related('trainer_ids','name', string='Status', type="char", relation="trainer.profile.info", readonly=1),
	'all_trainer':fields.many2one('trainer.profile.info', 'All Trainer',ondelete='cascade', help='Program', select=True),
	'class_sched':fields.many2one('class.info','Class',ondelete='cascade', help='Program', select=True),
	'mod_sched':fields.many2one('cs.module','Module',ondelete='cascade', help='Program', select=True),
	}
	_constraints = [(_class_start_notice, 'Error: Class Start Notice Cannot be Negative', ['Start Notice']),(_class_outstanding_notice, 'Error: Class Outstanding Notice Cannot be Negative', ['Outstanding Notice']),(_trainer_min_avail, 'Error: Trainer Min Avaliablity (%) Cannot be Negative', ['Avaliablity']),(_base_rate, 'Error: Base Rate ($ per hr) Cannot be Negative', ['Base Rate'])]
panel_info()

class assignment_schedule(osv.osv):
	_name = "assignment.schedule"
	_description = "Assignment Schedule"
	_columns = {
		'assigned_id': fields.many2one('panel.info',ondelete='cascade', help='Class Calendar', select=True),
		'all_trainer':fields.many2one('trainer.profile.info', 'All Trainer',ondelete='cascade', help='Trainer Info', select=True),
		'class_sched':fields.many2one('class.info','Class',ondelete='cascade', help='Class Calendar', select=True),
		'mod_sched':fields.many2one('cs.module','Module',ondelete='cascade', help='Module', select=True),
		'scheduled_date': fields.char('Scheduled Date'),
	}

#Trainer Schedule Details	
	def onchange_trainer_hist(self, cr, uid, ids, i_trainer, i_mod, context=None):
		val ={}
		sub_lines = []
		val.update({'scheduled_date':''})
		if i_trainer and i_mod:
			sql  ="select distinct c.start_date from class_info c, trainers_line t, cs_module cs, trainer_profile_info tp where t.trainers_line_id = c.id and cs.id =  c.module_id and tp.id = t.trainer_id and parent_id = 0 and cs.id = %s and tp.id = %s" % (i_mod, i_trainer)
			cr.execute(sql)
			itm = cr.fetchall()
			
			sub_lines = []
			for s in itm:
				val.update({'scheduled_date': s[0]})
			
			return {'value': val}
		else:
			return val
			
assignment_schedule()

class trainer(osv.osv):
	def _check_unique_trainer(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.trainer_id == self_obj.trainer_id and x.trainer_name == self_obj.trainer_name:
						return False
		return True
		
	def views_trainer(self,cr,uid,ids,context=None):
		trainer_id = self.browse(cr, uid, ids[0], context=context).trainer_name
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'trainer_profile_form')
		view_id = view_ref and view_ref[1] or False
		return {
		'type': 'ir.actions.act_window',
		'name': _('Trainer'),
		'res_model': 'trainer.profile.info',
		'view_type': 'form',
		'res_id': trainer_id and trainer_id.id or False, # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		}			
		
	_name = "trainer.line"
	_description = "This table is for keeping location data"
	_columns = {
	'trainer_id' : fields.many2one('panel.info', 'Panel',ondelete='cascade', help='Class Calendar', select=True),
	'trainer_name': fields.many2one('trainer.profile.info', 'Name', required=True,ondelete='cascade', help='Class Calendar', select=True),
	'trainer_status': fields.related('trainer_name','trainers_status', string='Status', type="char", relation="trainer.profile.info", readonly=1),
	'date_join': fields.date('Date Joined', required=True),
	}	
	_constraints = [(_check_unique_trainer, 'Error: Trainer Already Exists', ['Trainer Name'])]
trainer()

class asssign_schedule(osv.osv):
	_name = "assign.schedule.line"
	_description = "This table is for keeping location data"
	_columns = {
	'sche_id' : fields.many2one('panel.info','Pannel',ondelete='cascade', help='Class Calendar', select=True)
	}
asssign_schedule()

class setting_panel(osv.osv):
	_name = "setting.line"
	_description = "This table is for keeping location data"
	_columns = {
	'setting_id' : fields.many2one('panel.info','Pannel',ondelete='cascade', help='Class Calendar', select=True),
	
	}
setting_panel()

class trainer_profile_info(osv.osv):

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
		
	def _nationality_get(self, cr, uid, ids, context=None):
			ids = self.pool.get('res.country').search(cr, uid, [('name', '=', 'Singapore')], context=context)
			if ids:
				return ids[0]
			return False
			
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

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	def _mobile_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.mobile_no < 0:
				return False
		return True
		
	def _landline_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.landline_no < 0:
				return False
		return True
		
	def _office_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.office_no < 0:
				return False
		return True
		
	def _no_children(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.No_of_Children < 0:
				return False
		return True
		
	_name = "trainer.profile.info"
	_description = "This table is for keeping location data"
	_columns = {
	'location_id': fields.integer('Id',size=20),
	'name': fields.char('Name:', size=100,required=True, select=True),
	'image': fields.binary("Image"),
	'nric_name': fields.char('Name as in NRIC/FIN:', size=20),
	'nric': fields.char('NRIC/FIN:', size=10),
	'trainers_status': fields.selection((('Active','Active'),('InActive','InActive')),'Status', required=True, select=True),
	'date1': fields.date('Date Created', readonly='True'),
	'date2': fields.date('Date Created', readonly='True'),
	'trainer_id': fields.many2one('panel.info','Trainer',ondelete='cascade', help='Class Calendar', select=True),
	'trainer_status_display': fields.function(_trainer_status_display, readonly=1, type='char'),
	'trainer_status_display_1': fields.function(_trainer_status_display_1, readonly=1, type='char'),
	'assignment_avaliable': fields.one2many('trainers.assignment.avaliable','trainer_avail_id','Available', readonly=1),
	'assignment_current': fields.one2many('trainers.assignment.current','s_no','Current', readonly=1),
	'assignment_history': fields.one2many('trainers.assignment.history','s_no','History', readonly=1),
	'trainer_module_line': fields.one2many('trainer.module.line','trainers_id','Module',),
	#'personal_line': fields.one2many('personal.detail.module','personal_detail_id','Personal Details'),
	'nationality':fields.many2one('res.country', 'Nationality'),
	'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
	'race':fields.many2one('race', 'Race'),
	'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
	'Religion': fields.char('Religion', size=10),
	'No_of_Children':fields.integer('No of Children', size=2),
	'email_id': fields.char('Email', size=30),
	'addr_1': fields.text('Address', size=100),
	'mobile_no': fields.integer('Mobile', size=9),
	'landline_no': fields.integer('Landline', size=9),
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
    }
	_constraints = [(_check_unique_trainer_name, 'Error: Trainer Already Exists', ['Trainer Name']),(_check_unique_name_nric_fin, 'Error: Trainer NRIC/FIN Already Exists', ['NRIC/FIN']),(_check_unique_nric_fin, 'Error: Trainer NRIC/FIN Already Exists', ['NRIC/FIN']),(_check_unique_id, 'Error: Email Already Exist', ['Email']),(_mobile_no, 'Error: Mobile Number Cannot be Negative', ['Mobile']), (_landline_no, 'Error: Landline Number Cannot be Negative', ['Landline']), (_office_no, 'Error: Office Number Cannot be Negative', ['Office']), (_no_children, 'Error: Number of childrens Cannot be Negative', ['Children']), (_check_email, 'Error! Email is invalid.', ['work_email'])]
trainer_profile_info()

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

class current(osv.osv):
	_name ='trainers.assignment.current'
	_description ="Assignment Current Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'class':fields.char('Class',size=25),
	'class_code_current':fields.char('Class Code',size=25),
	'start_date_current':fields.date('Start Date'),
	'end_date_current':fields.date('End Date'),
	}
current	()

class assign_history(osv.osv):
	_name ='trainers.assignment.history'
	_description ="Assignment History Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'class':fields.char('Class',size=25),
	'class_code_history':fields.char('Class Code',size=25),
	'start_date_history':fields.date('Start Date'),
	'end_date_history':fields.date('End Date'),
	}
assign_history	()

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
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.now.datetime.now.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
	
	def onchange_dob(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.datetime.now().date()))
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
	'trainer_mod_status': fields.selection((('Active','Active'),('Pending','Pending')),'Status', required=True),
	'trainer_date':fields.date('Date'),
	}
	_constraints = [(_check_unique_module_name, 'Error: Module Already Exists', ['Module Name']), (_trainer_rate, 'Error: Trainer Rate Cannot be Negative', ['Trainer Rate'])]
trainer_module()


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

class qualification(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(qualification, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
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
qualification()

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

	_name = "work.exp.module"
	_description = "Work Experience Tab"
	_columns = {
	'work_id' : fields.integer('Id',size=20),
	's_no' : fields.integer('S.No',size=20,readonly=1),	
	'company':fields.char('Company',size=25),
	'industry':fields.char('Industry',size=25),
	'position':fields.char('Position',size=25),
	'year_from':fields.selection([(num, str(num)) for num in range(1900, (datetime.now().year)+1 )], 'Year From'),
	'year_to': fields.selection([(num, str(num)) for num in range(1900, (datetime.now().year)+1 )], 'Year To'),
	'key_responsibility':fields.char('Key Responsibilities'),
	'trg_specific':fields.boolean('Trg Specific'),
	}
	_constraints = [(_year_from_to, 'Error: Year To should be greater than Year From', ['Year'])]
work_exp()


class invoice(osv.osv):
	_name = "invoice.module"
	_description = "invoice Tab"
	_columns = {
	'invoice_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
invoice()
