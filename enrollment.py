from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class learner_info(osv.osv):

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	def views_enroll(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form')
		view_id = view_ref and view_ref[1] or False
		return {
		'type': 'ir.actions.act_window',
		'name': _('Learner'),
		'res_model': 'learner.info',
		'view_type': 'form',
		'res_id': ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		}
		
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.learner_name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.learner_name and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.learner_name and self_obj.learner_name.lower() in  lst:
				return False
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
		
	def _check_unique_adres(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.addr_1.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.addr_1 and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.addr_1 and self_obj.addr_1.lower() in  lst:
				return False
		return True		

	def _check_unique_number(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.mobile_no.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.mobile_no and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.mobile_no and self_obj.mobile_no.lower() in  lst:
				return False
		return True		
		
	def create(self,cr, uid, values, context=None):
		sub_lines = []
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		sub_lines.append( (0,0, {'date_created':fields.date.today(),'created_by':current_user['name'],
			'last_update':'-','last_update_by':'-','date_status_change':fields.date.today(),'status_change_by':current_user['name']}) )
		values.update({'history_learner_line': sub_lines})
		name = super(learner_info, self).create(cr, uid, values, context=context)
		return name
		
	"""def write(self,cr, uid, ids, values, context=None):
		sub_lines = []
		
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		for line in self.browse(cr, uid, ids, context=context):
			history_learner_line_id = self.browse(cr, uid, ids[0], context=context).history_learner_line or []

		num_of_his = len(history_learner_line_id)-1 
		staus_changed_by =   history_learner_line_id[num_of_his]['status_change_by']
		staus_changed_date =   history_learner_line_id[num_of_his]['date_status_change']
 
		if 'learner_status' in values:
			staus_changed_date = fields.date.today()
			staus_changed_by  = current_user['name']

		changes = values.keys()
		learner_list ={'learner_name': 'Name','learnerfull_name': 'Name as in NRIC/FIN','learner_nric':'NRIC','program_learner': 'Program','module_id': 'Module Name','history_learner_line': 'History','schedule_line':'Schedule',
				'class_code':'Class Code','start_date': 'Start Date', 'end_date': 'End Date','select_center': 'Select Center','select_module':'Select Module','date_1': 'Date',
				'module_line': 'enroll_module_line','check_line':'checklist','outstanding_line': 'outstanding','personal_details_line': 'personal details','nationality':'Nationality',
				'marital_status': 'Marital Status', 'race': 'Race','gender': 'Gender','birth_date':'Birth Date','date_1': 'Date', 'high_qualification': 'Highest Qualification',
				'language_proficiency':'Language Proficiency','emp_staus': 'Employement Status','company_name':'Company','desig_detail': 'Designation', 'sal_range': 'Salary Range','sponsor_ship':'Sponsorship',
				'email_id': 'Email','addr_1': 'Address','mobile_no':'Mobile','landline_no': 'Landline', 'office_no': 'Office','action_learn_line': 'Action','action_learner':'Action',
				'remarks_learner': 'Remarks','support_docs_learner':'Supported Documents','upload_learner': 'Uploads', 'date_action': 'Date of Action','action_taken_learner':'Action Taken By',
				'payment_history_line': 'Payment History','class_history_line': 'Class History','test_history_line':'Test History','test_score_line': 'Test Scores', 'qualification_line': 'Qualification & Awards',
				'assets_line': 'Assets','feedback_line':'Feedback', 'remarks_line':'Remarks','image':'Photo'}
		arr={}
		for i in range(len(changes)):
			if changes[i] in learner_list:
				arr[i] = learner_list[changes[i]]
  
		sub_lines.append( (0,0, {'date_created':history_learner_line_id[0]['date_created'],'created_by':history_learner_line_id[0]['created_by'],
			'last_update':fields.date.today(),'last_update_by':current_user['name'],'date_status_change':staus_changed_date,'status_change_by':staus_changed_by,'changes':arr.values()}) )
		values.update({'history_learner_line': sub_lines})
		name = super(learner_info, self).write(cr, uid, ids,values, context=context)
		return name """
		
		
	_name = "learner.info"
	_description = "This table is for keeping location data"
	_columns = {
		'location_id': fields.char('Id',size=20),
		'learner_name': fields.char('Name', size=100,required=True, select=True),
		'learnerfull_name': fields.char('Name as in NRIC/FIN', size=20),
		'learner_nric': fields.char('NRIC', size=20),
		'learner_status': fields.selection((('active','Active'),('Inactive','Inactive')),'Status'),
		'program_learner': fields.many2one('lis.program','Program',ondelete='cascade', help='Program', select=True, required=True),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True),
		'class_codel1':fields.char('Class'),
		'start_datel1':fields.date('Start'),
		'end_datel1':fields.date('End'),
		'select_learner_center':fields.selection((('Center A','Center A'),('Center B','Center B'),('Center C','Center C'),),'Select Center'),
		'outstanding_line': fields.one2many('outstanding.module','outstanding_id','outstanding'),
		'personal_details_line': fields.one2many('personal.module','personal_id','personal details'),
		'nationality':fields.selection((('Indian','Indian'),('American','American')),'Nationality'),
		'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
		'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'high_qualification':fields.selection((('No Formal Qualification & Lower Primary','No Formal Qualification & Lower Primary'),('Primary PSLE','Primary PSLE'),('Lower Secondary','Lower Secondary'),('N Level or equivalent','N Level or equivalent'),
		('O Level or equivalent','O Level or equivalent')),'Highest Qualification'),
		'language_proficiency':fields.boolean('Language Proficiency'),
		'emp_staus':fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
		'company_name':fields.selection((('ASZ','ASZ'),('HCL','HCL'),('CGI','CGI')),'Company'),
		'desig_detail':fields.selection((('Developer','Developer'),('Tester','Tester'),('HR','HR')),'Designation'),
		'sal_range':fields.selection((('10-15','10-15'),('15-25','15-25'),('25-50','25-50')),'Salary Range'),
		'sponsor_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
		'email_id': fields.char('Email', size=30),
		'addr_1': fields.text('Address', size=40),	
		'mobile_no': fields.char('Mobile', size=9),
		'landline_no': fields.char('Landline', size=9),
		'office_no': fields.char('Office', size=9),
		'action_learn_line': fields.one2many('action.learn.module','action_id','Action'),
		'action_learner': fields.selection((('Withdrawal','Withdrawal'),('Reassignment','Reassignment'),('Call','Call'),),'Action'),
		'remarks_learner': fields.char('Remarks'),
		'support_docs_learner': fields.char('Supported Documents'),
		'upload_learner': fields.char('Uploads'),
		'date_action':fields.date('Date of Action'),
		'action_taken_learner': fields.char('Action Taken By'),
		'payment_history_line': fields.one2many('payment.history.module','payment_id','Payment History'),
		'class_history_line': fields.one2many('class.history.module','class_id','Class History'),
		'test_history_line': fields.one2many('test.history.module','test_id','Test History'),
		'test_score_line': fields.one2many('test.score.module','test_score_id','Test Scores'),
		'qualification_line': fields.one2many('qualification.module','qualify_id','Qualification & Awards'),
		'assets_line': fields.one2many('assets.learner.module','asset_id','Assets'),
		'feedback_line': fields.one2many('feedback.module','feedback_id','Feedback'),
		'remarks_line': fields.one2many('remarks.module','remarks_id','Remarks'),
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
		'history_learner_line': fields.one2many('history.learner.module','history_id','History',limit=None),
		'schedule_line': fields.one2many('schedule.module','session_no','schedule'),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly='True'),
		'end_date':fields.date('End Date', readonly='True'),
		'select_center':fields.selection((('Center A','Center A'),('Center B','Center B'),('Center C','Center C'),),'Select Center'),
		'select_module':fields.selection((('Module 1','Module 1'),('Module 2','Module 2'),('Module 3','Module 3'),),'Select Module'),
		'date_1':fields.date('Date', readonly='True'),
		'module_line': fields.one2many('enroll.module.line','enroll_id','enroll_module_line'),
		'check_line': fields.one2many('checklist.module','checklist_id','checklist', readonly=1),
	}
	_constraints = [(_check_unique_name, 'Error: Learner Name Already Exists', ['learner_name']),(_check_unique_id, 'Error: Email ID Already Exists', ['email_id']),
	(_check_unique_adres, 'Error: Address Already Exists', ['addr_1']),(_check_unique_number, 'Error: Mobile Number Already Exists', ['mobile_no'])]
	
learner_info ()

class enroll_info(osv.osv):

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	def true_false_control(self, cr, uid, ids, context=None):
		if val:
			raise osv.except_osv(_('Warning', _('Test')))
			
	
			
			
		
	_name = "enroll.info"
	_description = "This table is for keeping location data"
	_columns = {
	    'location_id': fields.char('Id',size=20),
		'name': fields.char('Name', size=30,required=True, select=True),
		'full_name': fields.char('Name as in NRIC/FIN', size=30),
		'nric': fields.char('NRIC', size=30),
		'program_info': fields.selection((('prog A','Prog A'),('prog B','prog B')),'Program'),
		'module_line': fields.one2many('enroll.module.line','enroll_id','enroll_module_line'),
		'check_line': fields.one2many('checklist.module','checklist_id','checklist'),
		'schedule_line': fields.one2many('schedule.module','session_no','schedule'),
		'select_center':fields.selection((('Center A','Center A'),('Center B','Center B'),('Center C','Center C'),),'Select Center'),
		'select_module':fields.selection((('Module 1','Module 1'),('Module 2','Module 2'),('Module 3','Module 3'),),'Select Module'),
		'date_1':fields.date('Date', readonly='True'),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly='True'),
		'end_date':fields.date('End Date', readonly='True'),
		'personal_line': fields.one2many('personal.module','personal_id','Personal Details'),
		'nationality':fields.selection((('Indian','Indian'),('American','American')),'Nationality'),
		'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
		'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'high_qualification':fields.selection((('No Formal Qualification & Lower Primary','No Formal Qualification & Lower Primary'),('Primary PSLE','Primary PSLE'),('Lower Secondary','Lower Secondary'),('N Level or equivalent','N Level or equivalent'),
		('O Level or equivalent','O Level or equivalent')),'Highest Qualification'),
		'language_proficiency':fields.boolean('Language Proficiency'),
		'emp_staus':fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
		'company_name':fields.selection((('ASZ','ASZ'),('HCL','HCL'),('CGI','CGI')),'Company'),
		'desig_detail':fields.selection((('Developer','Developer'),('Tester','Tester'),('HR','HR')),'Designation'),
		'sal_range':fields.selection((('10-15','10-15'),('15-25','15-25'),('25-50','25-50')),'Salary Range'),
		'sponsor_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
		'email_id': fields.char('Email', size=30),
		'addr_1': fields.text('Address', size=40),	
		'mobile_no': fields.char('Mobile No', size=9),
		'landline_no': fields.char('Home Number', size=9),
		'office_no': fields.char('Office', size=9),
		'payment_line': fields.one2many('payment.module','payment_id','payment'),
		'history_line': fields.one2many('history.learner.module','history_id','history'),
		'image': fields.binary("Photo",
			help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
			string="Medium-sized photo", type="binary", multi="_get_image",
			store = {
				'enroll.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Medium-sized photo of the employee. It is automatically "\
				"resized as a 128x128px image, with aspect ratio preserved. "\
					"Use this field in form views or some kanban views."),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
			string="Smal-sized photo", type="binary", multi="_get_image",
			store = {
				'enroll.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Small-sized photo of the employee. It is automatically "\
				"resized as a 64x64px image, with aspect ratio preserved. "\
				"Use this field anywhere a small image is required."),
	}
		
enroll_info ()
	
	
class enroll_module_line(osv.osv):
	_name = "enroll.module.line"
	_description = "Module Tab"
	_columns = {
	'enroll_id' : fields.integer('Id',size=20), 
	'enroll_module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
	'enroll_code': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
	'no_of_hrs': fields.related('module_id','module_duration',type="float",relation="cs.module",string="Module Duration", readonly=1, required=True),
	
	}
	
enroll_module_line()


class checklist(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(checklist, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def import_Upload_Documents(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(data)) 

		# your treatment
		return
		
	_name ='checklist.module'
	_description ="checklist Tab"
	_columns = {
	'checklist_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,),
	'item':fields.char('Item',size=20,),
	'confirmation':fields.boolean('Confirmation',),
	'upload_docs':fields.binary('Upload Documents'),
	}
checklist ()


class schedule(osv.osv):
	_name ='schedule.module'
	_description ="schedule Tab"
	_columns = {
	'session_no' : fields.integer('Session No', size=20, readonly=1),
	'week_no' : fields.integer('Week No', size=20, readonly=1),
	'date_schd': fields.date('12/12/2014', readonly='True'),
	
	}
schedule ()

class personal(osv.osv):
	_name = "personal.module"
	_description = "Personal Details Tab"
	_columns = {
	'personal_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
personal()

class payment(osv.osv):
	_name = "payment.module"
	_description = "Payment Tab"
	_columns = {
	'payment_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
payment()

class history(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res



	_name = "history.learner.module"
	_description = "History Tab"
	_columns = { 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'history_id' : fields.integer('Id',size=20), 
	'date_created':fields.char('Date Created',size=20),
	'created_by':fields.char('Created By',size=20),
	'last_update':fields.char('Last Update',size=20),
	'last_update_by':fields.char('Last Update By',size=20),
	'date_status_change':fields.char('Date Of Status Change',size=20),
	'status_change_by':fields.char('Status Change By',size=20),
	'changes':fields.char('Changes',size=200)
	
	}	
	
	def on_change_module_id(self, cr, uid, ids, module_id):
		  module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		  return {'value': {'module_code': module_obj.module_code,'no_of_hrs':module_obj.module_duration}}
  
	def views(self,cr,uid,ids,context=None):
		  global globvar
		  globvar = 1
		  view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		  view_id = view_ref and view_ref[1] or False
		  prog_mod_obj = self.pool.get('program.module.line')
		  prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		  module_ids =[]
		  for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
		   module_ids.append(prog_module_line['module_id'].id)
		  ctx = dict(context)
		  #this will return product tree view and form view. 
		  ctx.update({
		   'ctx': True
		  })
		  return {
		  'type': 'ir.actions.act_window',
		  'name': _('Module'),
		  'res_model': 'cs.module',
		  'view_type': 'form',
		  'res_id': module_ids[0], # this will open particular product,
		  'view_id': view_id,
		  'view_mode': 'form',
		  'target': 'new',
		  'nodestroy': True,
		  'context': ctx,
  }
	
history()





class outstanding(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(outstanding, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name = "outstanding.module"
	_description = "outstanding Tab"
	_columns = {
	'outstanding_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'outs_item':fields.char('Item',size=20),
	'outs_confirmation':fields.boolean('Confirmation'),
	'outs_upload_docs':fields.char('Upload Documents', size=20),
	
	}	
outstanding()

class personal_details(osv.osv):
	_name = "personal.module"
	_description = "Personal Detail Tab"
	_columns = {
	'personal_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
personal_details()

class action_learn(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(action_learn, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name = "action.learn.module"
	_description = "Action Tab"
	_columns = {
	'action_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
action_learn()

class payment_history(osv.osv):
	_name = "payment.history.module"
	_description = "Payment History Tab"
	_columns = {
	'payment_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
payment_history()

class class_history(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(class_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name = "class.history.module"
	_description = "Class History Tab"
	_columns = {
	'class_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'program_name': fields.char('Program Name'),
	'module_name': fields.char('Module Name'),
	'class_code': fields.char('Class Code'),
	'Date_Commenced': fields.date('Date Commenced'),
	'Date_Completed': fields.date('Date Completed'),
	'empl_staus': fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
	'designa_detail':fields.selection((('Developer','Developer'),('Tester','Tester'),('HR','HR')),'Designation'),
	'sponsors_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
	}	
class_history()

class test_history(osv.osv):
	_name = "test.history.module"
	_description = "Test History Tab"
	_columns = {
	'test_id' : fields.integer('Id',size=20), 
	'test_type' : fields.char('Test',),
	'test_code' : fields.char('Test Code',),
	'test_date' : fields.date('Test Date'),
	'test_status' : fields.char('Test Status',),
	
	}	
test_history()

class test_score(osv.osv):
	_name = "test.score.module"
	_description = "Test Score Tab"
	_columns = {
	'test_score_id' : fields.integer('Id',size=20), 
	'test_score_type' : fields.char('Test',),
	'test_sc_code' : fields.char('Test Code',),
	'test_sc_date' : fields.date('Test Date'),
	'test_compre' : fields.char('Compr',),
	'test_conv' : fields.char('Conv',),
	'r_level' : fields.integer('R(Level)',),
	'r_score' : fields.integer('R(Score)',),
	'l_level' : fields.integer('L(Level)'),
	'l_score' : fields.integer('L(Score)'),
	's_level' : fields.integer('S(Level)'),
	's_score' : fields.integer('S(Score)'),
	'w_level' : fields.integer('W(Level)'),
	'w_score' : fields.integer('W(Score)'),
	'w_outcomes' : fields.char('W(Outcomes)'),
	'n_level' : fields.integer('N(Level)'),
	'n_score' : fields.integer('N(Score)'),
	'w_outcome1' : fields.char('W(Outcomes)'),
	
	}	
test_score()


class qualification(osv.osv):
	_name = "qualification.module"
	_description = "Qualifications & Awards Tab"
	_columns = {
	'qualify_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'qual_award_name' : fields.char('Qualification/Award Name'),
	'prog_name' : fields.char('Program Name'),
	'module_name' : fields.char('Module Name'),
	'class_code' : fields.char('Class Code'),
	'date_award' : fields.date('Date Awarded'),
	}	
qualification()


class assets(osv.osv):
	_name = "assets.learner.module"
	_description = "Assets Tab"
	_columns = {
	'asset_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
assets()

class feedback(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(feedback, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name = "feedback.module"
	_description = "Feedback Tab"
	_columns = {
	'feedback_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'feedback_type': fields.selection((('Negative','Negative'),('Complaint','Complaint'),('Positive','Positive')),'Feedback Type'),
	'description' : fields.char('Description'),
	'date_of_feedback' : fields.date('Date of Feedback'),
	'entered_by' : fields.char('Entered By'),
	
	}	
feedback()

class remarks(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(remarks, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name = "remarks.module"
	_description = "Remarks Tab"
	_columns = {
	'remarks_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'feedback_types': fields.selection((('Negative','Negative'),('Complaint','Complaint'),('Positive','Positive')),'Feedback Type'),
	'descriptions' : fields.char('Description'),
	'date_of_feedback' : fields.date('Date of Remarks'),
	'enter_by' : fields.char('Entered By'),
	
	}	
remarks()