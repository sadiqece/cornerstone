from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

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
		
	_name = "panel.info"
	_description = "This table is for keeping location data"
	_columns = {
	'trainer_line': fields.one2many('trainer.line','trainer_id','Trainers'),
	'asssign_schedule_line': fields.one2many('assign.schedule.line','sche_id','Assignment Schedules'),
	'setting_panel_line': fields.one2many('setting.line','setting_id','Settings'),
	'class_start_notice': fields.char('Class Start Notice', size=100),
	'class_outstanding_noitce': fields.char('Class Outstanding Noitce', size=100),
	'trainer_min_avail': fields.char('Trainer Min Avaliablity (%)', size=100),
	'base_rate': fields.char('Base Rate ($ per hr)'),
	'all_trainer':fields.many2one('trainer.line', 'All Trainer',ondelete='cascade', help='Program', select=True, required=True),
	'class_sched':fields.many2one('class.info','Class',ondelete='cascade', help='Program', select=True, required=True),
	'mod_sched':fields.many2one('trainer.module.line','Module',ondelete='cascade', help='Program', select=True, required=True),
	}
panel_info()

class trainer(osv.osv):
	_name = "trainer.line"
	_description = "This table is for keeping location data"
	_columns = {	
	'trainer_id' : fields.integer('Id',size=20),
	'trainer_name': fields.many2one('trainer.profile.info', 'Name'),
	'trainer_status': fields.char('Status', size=100),
	'date_join': fields.date('Date Joined', size=100),
	
	}
trainer()

class asssign_schedule(osv.osv):
	_name = "assign.schedule.line"
	_description = "This table is for keeping location data"
	_columns = {
	'sche_id' : fields.integer('Id',size=20),
	}
asssign_schedule()

class setting_panel(osv.osv):
	_name = "setting.line"
	_description = "This table is for keeping location data"
	_columns = {
	'setting_id' : fields.integer('Id',size=20),
	
	}
setting_panel()



class trainer_profile_info(osv.osv):
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		

	_name = "trainer.profile.info"
	_description = "This table is for keeping location data"
	_columns = {
	'location_id': fields.char('Id',size=20),
	'name': fields.char('Name', size=100,required=True, select=True),
	'nric_name': fields.char('Name as in NRIC/FIN', size=20),
	'nric': fields.char('NRIC', size=10),
	'trainers_status': fields.selection((('active','Active'),('Inactive','Inactive')),'Status'),
	'assignment_avaliable': fields.one2many('trainers.assignment.avaliable','s_no','Available', readonly=1),
	'assignment_current': fields.one2many('trainers.assignment.current','s_no','Current', readonly=1),
	'assignment_history': fields.one2many('trainers.assignment.history','s_no','History', readonly=1),
	'trainer_module_line': fields.one2many('trainer.module.line','trainers_id','Module',),
	#'personal_line': fields.one2many('personal.detail.module','personal_detail_id','Personal Details'),
	'nationality':fields.selection((('Indian','Indian'),('American','American')),'Nationality'),
	'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
	'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
	'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
	'Religion': fields.char('Religion', size=10),
	'No_of_Children':fields.selection((('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')),'No of Children'),
	'email_id': fields.char('Email', size=30),
	'addr_1': fields.text('Address', size=100),
	'mobile_no': fields.char('Mobile', size=10),
	'landline_no': fields.char('Landline', size=10),
	'office_no': fields.char('Office', size=10),
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
trainer_profile_info()

class avaliable(osv.osv):
	_name ='trainers.assignment.avaliable'
	_description ="Assignment Available Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'class':fields.char('Class',size=25),
	'class_code_avaliable':fields.char('Class Code',size=25),
	'start_date_avaliable':fields.date('Start Date'),
	'confirm':fields.char('Confirm?',size=10),
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
	_name = "trainer.module.line"
	_description = "Module Tab"
	_columns = {
	'trainers_id' : fields.integer('Id',size=20), 
	'trainer_module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
	'trainer_code': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
	'trainer_rate': fields.char('Trainer Rate', size=100),
	'trainer_mod_status': fields.selection((('active','Active'),('pending','Pending')),'Status'),
	'trainer_date':fields.date('Date'),
	}
	
trainer_module()


class personal_detail(osv.osv):
	_name = "personal.detail.module"
	_description = "Personal Details Tab"
	_columns = {
	'personal_detail_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
personal_detail()


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
	'year_awarded':fields.integer('Year Awarded',size=25),
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

	_name = "work.exp.module"
	_description = "Work Experience Tab"
	_columns = {
	'work_id' : fields.integer('Id',size=20),
	's_no' : fields.integer('S.No',size=20,readonly=1),	
	'company':fields.char('Company',size=25),
	'industry':fields.char('Industry',size=25),
	'position':fields.char('Position',size=25),
	'year_from':fields.integer('Year From'),
	'year_to': fields.integer('Year To'),
	'key_responsibility':fields.char('Key Responsibilities'),
	'trg_specific':fields.char('Trg Specific'),
	}	
work_exp()


class invoice(osv.osv):
	_name = "invoice.module"
	_description = "invoice Tab"
	_columns = {
	'invoice_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
invoice()
