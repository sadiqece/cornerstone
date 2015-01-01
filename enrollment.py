import datetime
from dateutil import relativedelta
from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import re


_logger = logging.getLogger(__name__)

'''def load_prog_Qualifi_award(self, cr, uid, ids, progid, context=None):
	#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(progid))
	p_obj = self.pool.get('lis.program')
	value_ids = p_obj.search(cr, uid, [(['ids'].id, '=', progid)])
	val ={}
	sub_lines = []
	for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
		sub_lines.append({'qual_award_name':prog_line['program_cert_achevied'].id,}) #'prog_name':prog_line['name'], 'module_name':prog_line['program_mod_line'
		
	val.update({'qualification_line': sub_lines})
	return {'value': val}	
	
	
def load_prog_Qualifi_award2(self, cr, uid, ids, progid, context=None):
	#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(progid))
	p_obj = self.pool.get('cs.module')
	value_ids = p_obj.search(cr, uid, [(['ids'].id, '=', progid)])
	val ={}
	sub_lines = []
	for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
		sub_lines.append({'qual_award_name':prog_line['module_certification'].id,}) #'prog_name':prog_line['name'], 'module_name':prog_line['program_mod_line'
		
	val.update({'qualification_line': sub_lines})
	return {'value': val}	'''	
	
class learner_info(osv.osv):

	'''def load_mod_Qualifi_award(self, cr, uid, ids, modid, context=None):
		#raise osv.except_osv(_('Warning!'),_('qualification award %s')%(progid))
		val ={}
		if modid:
			#sql = "select name, program_cert_achevied from lis_program where id = %s " % (progid)	
			sql = "select name, module_certification from cs_module where id = %s " % (modid)
		#	sql = "select name, class_code from class_info where id = %s " % (progid)
			cr.execute(sql)
			itm = cr.fetchall()
			sub_lines_prog = []
			for s in itm:
				#raise osv.except_osv(_('Warning!'),_('ewrewrewr %s')%(s[0]))
		#		sub_lines_prog.append({'prog_name':s[0], 'qual_award_name':s[1]})    
				sub_lines_prog.append({'module_id':s[0], 'qual_award_name':s[1]}) 
		#		sub_lines_prog.append({'class_code':s[0], 'class_code':s[1]}) 
				
			val.update({'qualification_line': sub_lines_prog})
			return {'value': val}'''
						
	def load_prog_Qualifi_award(self, cr, uid, ids, progid, context=None):
	  #raise osv.except_osv(_('Warning!'),_('qualification award %s')%(progid))
	  
	  p_obj = self.pool.get('program.show.do.module')
	  value_ids = p_obj.search(cr, uid, [('program_id', '=', progid)])
	  val2 ={}
	  sub_lines = []
	  for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
	   sub_lines.append({'outs_item':prog_line['master_show_do'].id, 'outs_confirmation':prog_line['supp_doc_req']})
	   
	  val2.update({'outstanding_line': sub_lines})
	  #return {'value': val2}
	  
	 
	  sub_lines_prog = []
	  if progid:
	   sql = "select name, program_cert_achevied from lis_program where id = %s " % (progid) 
	   cr.execute(sql)
	   itm = cr.fetchall()
	   for s in itm:
		#raise osv.except_osv(_('Warning!'),_('ewrewrewr %s')%(s[0]))
		sub_lines_prog.append({'prog_name':s[0], 'qual_award_name':s[1]})
		
	   val2.update({'qualification_line': sub_lines_prog})
	  # _logger.info('Installing chart of val2 %s', val2)
	  # return {'value': val2}
	 
		  
	  # class History 
	  sub_lines_prog = []
	  if progid:
	   sql = "select name from lis_program where id = %s " % (progid) 
	   cr.execute(sql)
	   itm = cr.fetchall()
	   for s in itm:
		#raise osv.except_osv(_('Warning!'),_('ewrewrewr %s')%(s))
		sub_lines_prog.append({'program_name':s[0]})
		
	   val2.update({'class_history_line': sub_lines_prog})	
	   _logger.info('Installing chart of val2 %s', val2)
	   return {'value': val2}
	  
	  
	  
	  '''sub_lines_prog = []
	  if progid:
	   sql = "select name from lis_program where id = %s " % (progid) 
	   cr.execute(sql)
	   itm = cr.fetchall()
	   for s in itm:
		#raise osv.except_osv(_('Warning!'),_('ewrewrewr %s')%(s[0]))
		sub_lines_prog.append({'program_name':s})
		
	   val2.update({'class_history_line': sub_lines_prog})
	  # _logger.info('Installing chart of val2 %s', val2)
	   return {'value': val2}	'''  
	  
	 		
						
	def onchange_populate_schedule(self, cr, uid, ids, m_id, context=None):
		sched_obj = self.pool.get('class.info')
		value_ids = sched_obj.search(cr, uid, [('module_id', '=', m_id)])
		res = {'value':{}}
		res['value']['class_code'] = 0
		res['value']['start_date'] = ''
		res['value']['end_date'] = ''
		for sched_line in sched_obj.browse(cr, uid, value_ids,context=context):
			res['value']['class_code'] = sched_line.id
			res['value']['start_date'] = sched_line.start_date
			res['value']['end_date'] = sched_line.end_date
			
		return res
		
	'''	sub_lines_mod = []
		if m_id:
		 sql = "select module_id, class_code, start_date, end_date from class_info where id = %s " % (m_id) 
		 cr.execute(sql)
		 itm = cr.fetchall()
		 for s in itm:
		  #raise osv.except_osv(_('Warning!'),_('ewrewrewr %s')%(s[0]))
		  sub_lines_mod.append({'module_name':s[0], 'class_code':s[1], 'Date_Commenced':s[2], 'Date_Completed':s[3]})
		
		 res.update({'class_history_line': sub_lines_mod})
		 _logger.info('Installing chart of res %s', res)
		 return res '''
			
			
			
	'''def onchange_populate_class_history(self, cr, uid, ids, mod_id, context=None):
				sched_obj = self.pool.get('class.info')
				value_ids = sched_obj.search(cr, uid, [('module_id', '=', mod_id)])
				res = {'value':{}}
				res['value']['class_code'] = 0
				res['value']['Date_Commenced'] = ''
				res['value']['Date_Completed'] = ''
				for sched_line in sched_obj.browse(cr, uid, value_ids,context=context):
					res['value']['class_code'] = sched_line.id
					res['value']['Date_Commenced'] = sched_line.Date_Commenced
					res['value']['Date_Completed'] = sched_line.Date_Completed
				return res '''				
		
	'''def load_prog_class_history(self, cr, uid, ids, progid, context=None):
		p_obj = self.pool.get('learner.info')
		value_ids = p_obj.search(cr, uid, [('module_id', '=', progid)])
		val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'program_name':prog_line['program_learner'].id, 'module_name':prog_line['module_id'], 'class_code':prog_line['class_code'],
			'Date_Commenced':prog_line['start_date'],'Date_Completed':prog_line['end_date']})
			
		val.update({'class_history_line': sub_lines})
		return {'value': val}		'''	
		
		
	'''def load_prog_Qualifi_award(self, cr, uid, ids, progid, context=None):
		#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(progid))
		p_obj = self.pool.get('lis.program')
		value_ids = p_obj.search(cr, uid, [(['ids'].id, '=', progid)])
		val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'qual_award_name':prog_line['program_cert_achevied'].id,}) #'prog_name':prog_line['name'], 'module_name':prog_line['program_mod_line'
			
		val.update({'qualification_line': sub_lines})
		return {'value': val} 
	
	
	def load_prog_Qualifi_award2(self, cr, uid, ids, progid, context=None):
		#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(progid))
		p_obj = self.pool.get('cs.module')
		value_ids = p_obj.search(cr, uid, [(['ids'].id, '=', progid)])
		val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'qual_award_name':prog_line['module_certification'].id,}) #'prog_name':prog_line['name'], 'module_name':prog_line['program_mod_line'
			
		val.update({'qualification_line': sub_lines})
		return {'value': val}		'''
	


	def load_prog_show_do2(self, cr, uid, ids, progid, context=None):
		p_obj = self.pool.get('program.show.do.module')
		value_ids = p_obj.search(cr, uid, [('program_id', '=', progid)])
		val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'item':prog_line['master_show_do'].id, 'confirmation':prog_line['supp_doc_req']})
			
		val.update({'check_line': sub_lines})
		return {'value': val}

	'''def load_prog_Qualifi_award(self, cr, uid, ids, progid, context=None):
		p_obj = self.pool.get('lis.program')
		value_ids = p_obj.search(cr, uid, [('id', '=', progid)])
		val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'qual_award_name':prog_line['program_cert_achevied'].id,}) #'prog_name':prog_line['name'], 'module_name':prog_line['program_mod_line'
			
		val.update({'qualification_line': sub_lines})
		return {'value': val}	'''

	def load_prog_show_do3(self, cr, uid, ids, progid, context=None):
		self.load_prog_Qualifi_award(cr, uid, ids, progid)
	#	load_prog_Qualifi_award(self, cr, uid, ids, progid)
	#	load_prog_Qualifi_award2(self, cr, uid, ids, progid)
		
		p_obj = self.pool.get('program.show.do.module')
		value_ids = p_obj.search(cr, uid, [('program_id', '=', progid)])
		val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'outs_item':prog_line['master_show_do'].id, 'outs_confirmation':prog_line['supp_doc_req']})
			
		val.update({'outstanding_line': sub_lines})
		return {'value': val} 
	
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
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, future date not allowed.                   ')}})
				return res
			return dob
			
	def _nationality_get(self, cr, uid, ids, context=None):
			ids = self.pool.get('res.country').search(cr, uid, [('name', '=', 'Singapore')], context=context)
			if ids:
				return ids[0]
			return False					
			
	def  ValidateEmail(self, cr, uid, ids, email_id):
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
	
		
		'''def load_prog_show_do4(self, cr, uid, ids, progid, context=None):
		p_obj = self.pool.get('program_test_line')
		value_ids = p_obj.search(cr, uid, [('program_id', '=', progid)])
		val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'test_type':prog_line['test_mod_line'].id, 'test_code':prog_line['test'], 'test_date':prog_line['test'],
			'test_status':prog_line['test']})
			
		val.update({'test_history': sub_lines})
		return {'value': val} 	'''
				
				
			
				
	
	_name = "learner.info"
	_description = "This table is for keeping location data"
	_columns = {
		'learner_id': fields.char('Id',size=20),
		'name': fields.char('Name', size=100,required=True, select=True),
		'learnerfull_name': fields.char('Name as in NRIC/FIN', size=20),
		'learner_nric': fields.char('NRIC', size=20),
		'learner_status': fields.selection((('active','Active'),('Inactive','Inactive')),'Status'),
		'program_learner': fields.many2one('lis.program','Program', 'program_show_do_line', ondelete='cascade', help='Program', select=True, required=True),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True),
		#'class_codel1':fields.char('Class'),
		#'start_datel1':fields.date('Start'),
		#'end_datel1':fields.date('End'),
		'select_learner_center':fields.selection((('Center A','Center A'),('Center B','Center B'),('Center C','Center C'),),'Select Center'),
		'outstanding_line': fields.one2many('outstanding.module','outstanding_id','outstanding'),
		'personal_details_line': fields.one2many('personal.module','personal_id','personal details'),
		'nationality':fields.many2one('res.country', 'Nationality'),
		'marital_status':fields.selection((('Single','Single'),('Married','Married'),('Widow','Widow')),'Marital Status'),
		'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'high_qualification':fields.selection((('No Formal Qualification & Lower Primary','No Formal Qualification & Lower Primary'),('Primary PSLE','Primary PSLE'),('Lower Secondary','Lower Secondary'),('N Level or equivalent','N Level or equivalent'),
		('O Level or equivalent','O Level or equivalent'),('A Level or equivalent','A Level or equivalent'),('ITE Skills Certification (ISC)','ITE Skills Certification (ISC)'),('Higher NITEC','Higher NITEC'),('NITEC/Post Nitec','NITEC/Post Nitec'),
		('Polytechnic Diploma','Polytechnic Diploma'),('WSQ Diploma','WSQ Diploma'),('Professional Qualification & Other Diploma','Professional Qualification & Other Diploma'),('University First Degree','University First Degree'),
		('University Post-graduate Diploma & Degree/Master/Doctorate','University Post-graduate Diploma & Degree/Master/Doctorate'),('WSQ Certificate','WSQ Certificate'),('WSQ Higher Certificate','WSQ Higher Certificate'),('WSQ Advance Certificate','WSQ Advance Certificate'),
		('WSQ Diploma','WSQ Diploma'),('WSQ Specialist Diploma','WSQ Specialist Diploma'),('WSQ Graduate Diploma','WSQ Graduate Diploma'),('Others','Others'),('Not Reported','Not Reported')),'Highest Qualification'),
		'language_proficiency':fields.boolean('Language Proficiency'),
		'emp_staus':fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
		'company_name':fields.selection((('ASZ','ASZ'),('HCL','HCL'),('CGI','CGI')),'Company'),
		#'company_name':fields.many2one('cornerstone.company','company_name','Company'),
		'desig_detail':fields.selection((('Developer','Developer'),('Tester','Tester'),('HR','HR')),'Designation'),
		'sal_range':fields.selection((('10-15','10-15'),('15-25','15-25'),('25-50','25-50')),'Salary Range'),
		'sponsor_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
		'email_id': fields.char('Email', size=30),
		'addr_1': fields.text('Address', size=40),	
		'mobile_no': fields.char('Mobile', size=9),
		'landline_no': fields.integer('Landline', size=9),
		'office_no': fields.integer('Office', size=9),
		'action_learn_line': fields.one2many('action.learn.module','action_id','Action'),
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
		'history_learner_line': fields.one2many('history.learner.module','history_id','History'),
		'schedule_line': fields.one2many('schedule.module','session_no','schedule'),
		'class_code':fields.many2one('class.info', 'Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly=1),
		'end_date':fields.date('End Date', readonly=1),
		'select_center':fields.selection((('Center A','Center A'),('Center B','Center B'),('Center C','Center C'),),'Select Center'),
		'select_module':fields.many2one('cs.module', 'Select Module', ondelete='cascade', help='Module', select=True),
		'date_1':fields.date('Date', readonly='True'),
		'module_line': fields.one2many('enroll.module.line','enroll_id','Module'),
		'check_line': fields.one2many('checklist.module','checklist_id','checklist'),
	}
	_constraints = [(_check_unique_id, 'Error: Email ID Already Exists', ['email_id']),(_check_unique_number, 'Error: Mobile Number Already Exists', ['mobile_no'])]
	
	def on_change_select_module(self, cr, uid, ids, select_module):
		module_obj = self.pool.get('cs.module').browse(cr, uid, select_module)
		return {'value': {'module_code': module_obj.module_code,'no_of_hrs':module_obj.module_duration}}
	
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
			
	
			
	def  ValidateEmail(self, cr, uid, ids, email_id):
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_id) != None:
			return True
		else:
			raise osv.except_osv('Invalid Email', 'Please enter a valid email address')
				
				
	def _nationality_get(self, cr, uid, ids, context=None):
		ids = self.pool.get('res.country').search(cr, uid, [('name', '=', 'Singapore')], context=context)
		#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(ids[0]))
		if ids:
			return ids[0]
		return False			
						
		
	'''def _check_unique_id(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.email_id.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.email_id and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.email_id and self_obj.email_id.lower() in  lst:
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
		return True	'''
		
			
		
	_name = "enroll.info"
	_description = "This table is for keeping location data"
	_columns = {
	    'location_id': fields.char('Id',size=20),
		'name': fields.char('Name', size=30,required=True, select=True),
		'full_name': fields.char('Name as in NRIC/FIN', size=30),
		'nric': fields.char('NRIC', size=30),
		'program_info': fields.selection((('prog A','Prog A'),('prog B','prog B')),'Program'),
		'module_line': fields.one2many('enroll.module.line','module_id','Module'),
		'check_line': fields.one2many('checklist.module','checklist_id','checklist'),
		'schedule_line': fields.one2many('schedule.module','session_no','schedule'),
		'select_center':fields.selection((('Center A','Center A'),('Center B','Center B'),('Center C','Center C'),),'Select Center'),
		'select_module':fields.selection((('Module 1','Module 1'),('Module 2','Module 2'),('Module 3','Module 3'),),'Select Module'),
		'date_1':fields.date('Date', readonly='True'),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly='True'),
		'end_date':fields.date('End Date', readonly='True'),
		'personal_line': fields.one2many('personal.module','personal_id','Personal Details'),
		'nationality':fields.many2one('res.country', 'Nationality'),
		'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
		'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'high_qualification':fields.selection((('No Formal Qualification & Lower Primary','No Formal Qualification & Lower Primary'),('Primary PSLE','Primary PSLE'),('Lower Secondary','Lower Secondary'),('N Level or equivalent','N Level or equivalent'),
		('O Level or equivalent','O Level or equivalent'),('A Level or equivalent','A Level or equivalent'),('ITE Skills Certification (ISC)','ITE Skills Certification (ISC)'),('Higher NITEC','Higher NITEC'),('NITEC/Post Nitec','NITEC/Post Nitec'),
		('Polytechnic Diploma','Polytechnic Diploma'),('WSQ Diploma','WSQ Diploma'),('Professional Qualification & Other Diploma','Professional Qualification & Other Diploma'),('University First Degree','University First Degree'),
		('University Post-graduate Diploma & Degree/Master/Doctorate','University Post-graduate Diploma & Degree/Master/Doctorate'),('WSQ Certificate','WSQ Certificate'),('WSQ Higher Certificate','WSQ Higher Certificate'),('WSQ Advance Certificate','WSQ Advance Certificate'),
		('WSQ Diploma','WSQ Diploma'),('WSQ Specialist Diploma','WSQ Specialist Diploma'),('WSQ Graduate Diploma','WSQ Graduate Diploma'),('Others','Others'),('Not Reported','Not Reported')),'Highest Qualification'),
		'language_proficiency':fields.boolean('Language Proficiency'),
		'emp_staus':fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
		'company_name':fields.selection((('ASZ','ASZ'),('HCL','HCL'),('CGI','CGI')),'Company'),
		'desig_detail':fields.selection((('Developer','Developer'),('Tester','Tester'),('HR','HR')),'Designation'),
		'sal_range':fields.selection((('10-15','10-15'),('15-25','15-25'),('25-50','25-50')),'Salary Range'),
		'sponsor_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
		'email_id': fields.char('Email', size=30),
		'addr_1': fields.text('Address', size=40),	
		'mobile_no': fields.integer('Mobile No', size=9),
		'landline_no': fields.integer('Home Number', size=9),
		'office_no': fields.integer('Office', size=9),
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
	'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
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
		fileobj.write(base64.decodestring(upload_docs)) 

		# your treatment
		return
		
	_name ='checklist.module'
	_description ="checklist Tab"
	_columns = {
	'checklist_id' : fields.integer('Id',size=20, readonly=1), 
	's_no' : fields.integer('S.No',size=20, readonly=1),
	#'program_id': fields.one2many('program.show.do.module', 'program_id', ondelete='cascade', help='Program'),
	#'master_show_do':fields.many2one('master.show.do', 'Item', ondelete='cascade', help='Show & Do', select=True, required=True),
	#'item':fields.char('Item', readonly=1), 
	'item':fields.many2one('master.show.do', 'Item', ondelete='cascade'),
	'confirmation':fields.boolean('Confirmation' , readonly=1),
	'upload_docs':fields.binary('Upload Documents'),
	}

	def on_change_program_id(self, cr, uid, ids, program_id):
		module_obj = self.pool.get('lis.program').browse(cr, uid, program_id)
		return {'value': {'item': module_obj.item, 'confirmation': module_obj.confirmation}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('checklist.module')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['program_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'item': _('item'),
		'res_model': 'lis.program',
		'view_type': 'form',
		'res_id': module_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}
			
checklist()


class schedule(osv.osv):
	
	_name ='schedule.module'
	_description ="schedule Tab"
	_columns = {
	'session_no' : fields.integer('Session No', size=10, readonly=1),
	'week_no' : fields.integer('Week No', size=20, readonly=1),
	'date_schd': fields.date('12/12/2014', readonly='True'),
	
	}
schedule ()

class personal(osv.osv):
	_name = "personal.module"
	_description = "Personal Details Tab"
	_columns = {
	'personal_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20, readonly=1),
	
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


class outstanding(osv.osv):	

	def import_Upload_Documents1(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(outs_upload_docs)) 

		# your treatment
		return		

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
	'outstanding_id' : fields.integer('Id',size=20, readonly=1), 
	's_no' : fields.integer('S.No',size=20, readonly=1),
	#'outs_item':fields.char('Item'),
	'outs_item':fields.many2one('master.show.do', 'Item', ondelete='cascade', readonly=1),
	'outs_confirmation':fields.boolean('Confirmation', readonly=1),
	'outs_upload_docs':fields.binary('Upload Documents', size=20),
	}
	
	def on_change_program_id(self, cr, uid, ids, program_id):
		module_obj = self.pool.get('lis.program').browse(cr, uid, program_id)
		return {'value': {'outs_item': module_obj.outs_item, 'outs_confirmation': module_obj.outs_confirmation}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('outstanding.module')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['program_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'item': _('outs_item'),
		'res_model': 'lis.program',
		'view_type': 'form',
		'res_id': module_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,	
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
				
	def _current_user(self, cr, uid, ids, context=None):
		return uid		
				
		
	def import_Upload_action(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(upload_learner)) 

		# your treatment
		return	
		
		
	'''def _get_attachments(self, cr, uid, ids, field_name, arg, context):
		res = {}
		attach_pool = self.pool.get('ir.attachment')
		print "IDs: ", ids
		attachs = attach_pool.search(cr, uid, args = [('res_id', 'in', ids)])
		print "Attachs: ", attachs
		return res '''


	_name = "action.learn.module"
	_description = "Action Tab"
	_columns = {
	'action_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'action_learner': fields.selection((('Withdrawal','Withdrawal'),('Reassignment','Reassignment'),('Call','Call'),),'Action'),
	'remarks_learner': fields.char('Remarks'),
	'support_docs_learner': fields.char('Supported Documents'),
	#'upload_learner': fields.function(_get_attachments, method=True, type='char', string='Uploads'),
	'upload_learner': fields.binary('Uploads'),
	'support_docs_learner': fields.related('upload_learner','support_docs_learner',type="char",relation="action.learn.module",string="Supported Documents"),
	'date_action':fields.date('Date of Action'),
	'action_taken_learner': fields.many2one('res.users','Action Taken By'),
	
	}	
	_defaults = {
	   'action_taken_learner': _current_user,
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
	
	'''def onchange_populate_class_history(self, cr, uid, ids, mod_id, context=None):
		sched_obj = self.pool.get('class.info')
		value_ids = sched_obj.search(cr, uid, [('module_id', '=', mod_id)])
		res = {'value':{}}
		res['value']['class_code'] = 0
		res['value']['Date_Commenced'] = ''
		res['value']['Date_Completed'] = ''
		for sched_line in sched_obj.browse(cr, uid, value_ids,context=context):
			res['value']['class_code'] = sched_line.id
			res['value']['Date_Commenced'] = sched_line.Date_Commenced
			res['value']['Date_Completed'] = sched_line.Date_Completed
		return res '''
		
		
	_name = "class.history.module"
	_description = "Class History Tab"
	_columns = {
	'class_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	#'program_name': fields.char('Program Name'),
	#'module_name': fields.char('Module Name'),
	'program_name': fields.many2one('lis.program','Program Name', 'program_learner', ondelete='cascade', help='Program', select=True),
	'module_name':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True),
	'class_code':fields.many2one('class.info', 'Class Code'),
	#'Date_Commenced': fields.date('Date Commenced'),
	#'Date_Completed': fields.date('Date Completed'),
	'start_date': fields.date('Date Commenced'),
	'end_date': fields.date('Date Completed'),
	'empl_staus': fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
	'designa_detail':fields.selection((('Developer','Developer'),('Tester','Tester'),('HR','HR')),'Designation'),
	'sponsors_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
	}
	
	def on_change_prog_name(self, cr, uid, ids, program_name):
		module_obj = self.pool.get('lis.program').browse(cr, uid, program_name)
		return {'value': {'program_name': module_obj.program_name}}	
		
		
	def on_change_module_name(self, cr, uid, ids, module_name):
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_name)
		return {'value': {'module_name': module_obj.module_name}}	

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

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(qualification, self).read(cr, uid, ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res		
		


	_name = "qualification.module"
	_description = "Qualifications & Awards Tab"
	_columns = {
	'qualify_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20),
	#'qual_award_name' : fields.many2one('lis.program', 'Qualification /Award Name', ondelete='cascade', readonly=1),
	'qual_award_name' : fields.char('Qualification /Award Name', size=30),
	'prog_name' : fields.one2many('lis.program', 'name', 'Program Name', ondelete='cascade', help='Program', select=True),
	'module_name':fields.many2one('cs.module','Module Name', ondelete='cascade', help='Module', select=True),
	'class_code':fields.many2one('class.info', 'Class Code'),
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

	#def _current_user(self, cr, uid, ids, context=None):
	#	return self.pool.get('res.users').browse(cr, uid,uid, context=context),

	def _current_user(self, cr, uid, ids, context=None):
		return uid
		#ids = self.pool.get('res.users').search(cr, uid, context=context)
		#if ids:
		#	return ids[0]
		#return False
		
	_name = "feedback.module"
	_description = "Feedback Tab"
	_columns = {
	'feedback_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'feedback_type': fields.selection((('Negative','Negative'),('Complaint','Complaint'),('Positive','Positive')),'Feedback Type'),
	'description' : fields.char('Description'),
	'date_of_feedback' : fields.date('Date of Feedback'),
	'entered_by' : fields.many2one('res.users','Entered By'),
	}	
	
	_defaults = {
	   'entered_by': _current_user,
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
		
		
	#def _current_user(self, cr, uid, ids, context=None):
	#	return self.pool.get('res.users').browse(cr, uid,uid, context=context),

	def _current_user(self, cr, uid, ids, context=None):
		return uid
		#ids = self.pool.get('res.users').search(cr, uid, context=context)
		#if ids:
		#	return ids[0]
		#return False
		
	_name = "remarks.module"
	_description = "Remarks Tab"
	_columns = {
	'remarks_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'descriptions' : fields.char('Description'),
	'date_of_remarks' : fields.date('Date of Remarks'),
	'enter_by' :  fields.many2one('res.users','Entered By'),
	
	}	
	
	_defaults = {
	   'enter_by': _current_user,
	   }
remarks()