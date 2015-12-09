from openerp.osv import fields, osv
from openerp.tools.translate import _

class add_program_wizard(osv.osv_memory):

	#Learner 11 Tabs Display		
	def enroll(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form_wizard')
		view_id = view_ref and view_ref[1] or False
		return {
		'type': 'ir.actions.act_window',
		'name': _('Add Program'),
		'res_model': 'learner.info',
		'view_type': 'form',
		#'res_id': ln_ids[0], # this will open particular Learner Details,
		'view_id': view_id,
		'view_mode': 'form',
		'nodestroy': True,
		}

	_name = 'add.program.wizard'
	_description = 'Add Program Wizard'    
	_columns = { 
		'name': fields.char('Id',size=20),  
	} 
	
add_program_wizard()

class learner_profile_wizard(osv.osv):

	def load_module_groups(self, cr, uid, ids, progid, context=None):

		val ={}	
		sub_lines = []
		set_group_as_sel_1 = False
		set_group_as_sel_2 = False
		set_group_as_sel_3 = False
		set_group_as_sel_4 = False
		set_group_as_sel_5 = False
		set_group_as_sel_6 = False
		
		
		set_module_as_1 =''
		set_module_as_2 = ''
		set_module_as_3 = ''
		set_module_as_4 = ''
		set_module_as_5 = ''
		set_module_as_6 = ''
		
		for program in self.pool.get('lis.program').browse(cr,uid, [progid], context=context):
			if program.no_of_mod_gp:
				no_of_mod_gp = program.no_of_mod_gp
			#Group Selectable
			if program.set_group_as_sel_1:
				set_group_as_sel_1 = program.set_group_as_sel_1
			if program.set_group_as_sel_2:
				set_group_as_sel_2 = program.set_group_as_sel_2
			if program.set_group_as_sel_3:
				set_group_as_sel_3 = program.set_group_as_sel_3
			if program.set_group_as_sel_4:
				set_group_as_sel_4 = program.set_group_as_sel_4
			if program.set_group_as_sel_5:
				set_group_as_sel_5 = program.set_group_as_sel_5
			if program.set_group_as_sel_6:
				set_group_as_sel_6 = program.set_group_as_sel_6
			#Group Name
			if program.mod_gp_name_1:
				val.update({'mod_gp_name_1': program.mod_gp_name_1})
			if program.mod_gp_name_2:
				val.update({'mod_gp_name_2': program.mod_gp_name_2})
			if program.mod_gp_name_3:
				val.update({'mod_gp_name_3': program.mod_gp_name_3})
			if program.mod_gp_name_4:
				val.update({'mod_gp_name_4': program.mod_gp_name_4})
			if program.mod_gp_name_5:
				val.update({'mod_gp_name_5': program.mod_gp_name_5})
			if program.mod_gp_name_6:
				val.update({'mod_gp_name_6': program.mod_gp_name_6})
			#Module Selectable
			if program.set_module_as_1:
				set_module_as_1 = program.set_module_as_1
			if program.set_module_as_2:
				set_module_as_2 = program.set_module_as_2
			if program.set_module_as_3:
				set_module_as_3 = program.set_module_as_3
			if program.set_module_as_4:
				set_module_as_4 = program.set_module_as_4
			if program.set_module_as_5:
				set_module_as_5 = program.set_module_as_5
			if program.set_module_as_6:
				set_module_as_6 = program.set_module_as_6
			#Min Value
			if program.min_no_modules_1:
				val.update({'min_no_modules_1': program.min_no_modules_1})
			if program.min_no_modules_2:
				val.update({'min_no_modules_2': program.min_no_modules_2})
			if program.min_no_modules_3:
				val.update({'min_no_modules_3': program.min_no_modules_3})
			if program.min_no_modules_4:
				val.update({'min_no_modules_4': program.min_no_modules_4})
			if program.min_no_modules_5:
				val.update({'min_no_modules_5': program.min_no_modules_5})
			if program.min_no_modules_6:
				val.update({'min_no_modules_6': program.min_no_modules_6})
			#Max Value
			if program.max_no_modules_1:
				val.update({'max_no_modules_1': program.max_no_modules_1})
			if program.max_no_modules_2:
				val.update({'max_no_modules_2': program.max_no_modules_2})
			if program.max_no_modules_3:
				val.update({'max_no_modules_3': program.max_no_modules_3})
			if program.max_no_modules_4:
				val.update({'max_no_modules_4': program.max_no_modules_4})
			if program.max_no_modules_5:
				val.update({'max_no_modules_5': program.max_no_modules_5})
			if program.max_no_modules_6:
				val.update({'max_no_modules_6': program.max_no_modules_6})
				
#Module Group Selectable
		#1			
		if set_group_as_sel_1 == True:
			val.update({'set_group_as_sel_1': True})
		elif set_group_as_sel_1 == False:
			val.update({'set_group_as_sel_1': False})
		#2
		if set_group_as_sel_2 == True:
			val.update({'set_group_as_sel_2': True})
		elif set_group_as_sel_2 == False:
			val.update({'set_group_as_sel_2': False})
		#3
		if set_group_as_sel_3 == True:
			val.update({'set_group_as_sel_3': True})
		elif set_group_as_sel_3 == False:
			val.update({'set_group_as_sel_3': False})
		#4
		if set_group_as_sel_4 == True:
			val.update({'set_group_as_sel_4': True})
		elif set_group_as_sel_4 == False:
			val.update({'set_group_as_sel_4': False})
		#5
		if set_group_as_sel_5 == True:
			val.update({'set_group_as_sel_5': True})
		elif set_group_as_sel_5 == False:
			val.update({'set_group_as_sel_5': False})
		#6
		if set_group_as_sel_6 == True:
			val.update({'set_group_as_sel_6': True})
		elif set_group_as_sel_6 == False:
			val.update({'set_group_as_sel_6': False})
			
#No Of Module Groups
		if no_of_mod_gp == '1':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': False})
			val.update({'no_module_box3': False})
			val.update({'no_module_box4': False})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '2':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': False})
			val.update({'no_module_box4': False})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '3':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': False})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '4':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': True})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '5':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': True})
			val.update({'no_module_box5': True})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '6':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': True})
			val.update({'no_module_box5': True})
			val.update({'no_module_box6': True})

#Set Module Selectable
		#1
		if set_module_as_1 == 'Selectable':
			val.update({'set_module_select_1': True})
			
		elif set_module_as_1 != 'Selectable':
			val.update({'set_module_select_1': False})
			
		#2
		if set_module_as_2 == 'Selectable':
			val.update({'set_module_select_2': True})
		elif set_module_as_2 != 'Selectable':
			val.update({'set_module_select_2': False})
		#3
		if set_module_as_3 == 'Selectable':
			val.update({'set_module_select_3': True})
		elif set_module_as_3 != 'Selectable':
			val.update({'set_module_select_3': False})
		#4
		if set_module_as_4 == 'Selectable':
			val.update({'set_module_select_4': True})
		elif set_module_as_4 != 'Selectable':
			val.update({'set_module_select_4': False})
		#5
		if set_module_as_5 == 'Selectable':
			val.update({'set_module_select_5': True})
		elif set_module_as_5 != 'Selectable':
			val.update({'set_module_select_5': False})
		#6
		if set_module_as_6 == 'Selectable':
			val.update({'set_module_select_6': True})
		elif set_module_as_6 != 'Selectable':
			val.update({'set_module_select_6': False})
			
# 1=====	
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id', '=', progid)])	
		sub_lines = []		
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_1 != 'Selectable':
				sub_lines.append({'module_id':prog_line['module_id'].id, 'check_module_select_1':False})
			else:
				sub_lines.append({'module_id':prog_line['module_id'].id, 'check_module_select_1':True})
		val.update({'learner_mod_line': sub_lines})
# 2 ====		
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_2', '=', progid)])
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_2 != 'Selectable':
				sub_lines.append({'module_id_2':prog_line['module_id_2'].id, 'check_module_select_2':False})
			else:
				sub_lines.append({'module_id_2':prog_line['module_id_2'].id, 'check_module_select_2':True})
		val.update({'learner_mod_line_2': sub_lines})
# 3 ====
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_3', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_3 != 'Selectable':
				sub_lines.append({'module_id_3':prog_line['module_id_3'].id, 'check_module_select_3':False})
			else:
				sub_lines.append({'module_id_3':prog_line['module_id_3'].id, 'check_module_select_3':True})
		val.update({'learner_mod_line_3': sub_lines})
# 4 ======		
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_4', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_4 != 'Selectable':
				sub_lines.append({'module_id_4':prog_line['module_id_4'].id, 'check_module_select_4':False})
			else:
				sub_lines.append({'module_id_4':prog_line['module_id_4'].id, 'check_module_select_4':True})
		val.update({'learner_mod_line_4': sub_lines})		
# 5 ======		
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_5', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_5 != 'Selectable':
				sub_lines.append({'module_id_5':prog_line['module_id_5'].id, 'check_module_select_5':False})
			else:
				sub_lines.append({'module_id_5':prog_line['module_id_5'].id, 'check_module_select_5':True})
		val.update({'learner_mod_line_5': sub_lines})
# 6 =======
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_6', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_6 != 'Selectable':
				sub_lines.append({'module_id_6':prog_line['module_id_6'].id, 'check_module_select_6':False})
			else:
				sub_lines.append({'module_id_6':prog_line['module_id_6'].id, 'check_module_select_6':True})
		val.update({'learner_mod_line_6': sub_lines})
		#return {'value': val}

#Module Status
	def _learner_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['learner_status']
		return res

	def _learner_status_display_2(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['learner_status']
		return res
		
	def _learner_status_display_3(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['learner_status']
		return res
		
		
# Payment Module Function for Grand Total
	#_inherit = "payment.module"
	def _amount(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_learner:
				total += line.cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
# Payment Test Function for Grand Total
	#_inherit = "payment.module"
	def _amount_test(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_test_learner:
				total += line.test_cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
	def _calculate_total_checklist(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = line.checklist_tab or []
			_logger.info("total id %s",mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
		return res
		
	def _learner_name(self, cr, uid, values, context=None):
		obj_res_hist = self.pool.get('learner.info')
		
		for ch in values:
			sql="select name from learner_info where id = %s " % (ch['learner_id'])
			cr.execute(sql)
			itm = cr.fetchall()
			for s in itm:
				ln = s[0]

			vals = {
				'learner_program_id':ch['learner_id'],
				'name': ln,
			}
			obj_res_hist.create(cr, uid, vals, context=context)
		return True
		
	def create(self, cr, uid, ids, context=None):
	
		self._learner_name( cr, uid, ids, id)
		return id
		
#Table Learner Info
	_name = "learner.profile.wizard"
	_description = "Learner Profile Wizard"
	_columns = {
		'learner_program_id': fields.char('Id',size=20),
		'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True,),
		#'name': fields.many2one('learner.name', 'Name', required=True, size=100, type='char'),
		#'learnerfull_name': fields.many2one('learner.name.nric', 'Name as in NRIC/FIN', required=True, size=100),
		#'learner_nric': fields.many2one('learner.nric', 'NRIC', size=7,required=True, help='Add one Prefix and one Suffix'),
		'name': fields.char('Name', size=100, select=True, readonly=1),
		'learnerfull_name': fields.char('Name as in NRIC/FIN', size=100,required=True),
		'nationality':fields.selection((('Singapore','Singapore'),('Malaysia','Malaysia'),('South Korea','South Korea'),('North Korea','North Korea'),('India','India'),('Indonesia','Indonesia'),('Vietnam','Vietnam')),'Nationality',required=True),
		'learner_nric': fields.char('NRIC', size=9,  help='Add one Prefix and one Suffix'),
		'learner_non_nric': fields.char('Non-NRIC', size=44,  help='Add one Prefix and one Suffix'),
		'learner_status': fields.selection((('Active','Active'),('InActive','InActive'),('Complete','Complete'),('InComplete','InComplete'),('Blocked','Blocked')),'Status', required=True),
		'learner_status_display_1': fields.function(_learner_status_display_1, readonly=1, type='char'),
		'learner_status_display_2': fields.function(_learner_status_display_2, readonly=1, type='char'),
		'learner_status_display_3': fields.function(_learner_status_display_3, readonly=1, type='char'),
		'date1': fields.date('Date Created', readonly='True'),
		'date2': fields.date('Date Created', readonly='True'),
		'program_learner': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True,required=True),
		'selected_program': fields.many2one('learner.info', 'Selected Programs by Learner', ondelete='cascade', help='Learner', Select=True),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, store=True),
		#checklist Tab
		'checklist_tab': fields.one2many('checklist.module','checklist_id','checklist'),
		#Schedule Tab
		'toggling': fields.selection((('Class Schedule','Class Schedule'),('Test Schedule','Test Schedule')),'Select Schedule'),
		'class_type_schedule': fields.boolean('Class Schedule'),
		'test_type_schedule': fields.boolean('Test Schedule'),
		'select_center':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'class_schedule_line': fields.one2many('class.schedule.module','session_no','Class Schedule'),
		'test_schedule_line': fields.one2many('test.schedule.module','class_info_id','Test Schedule'),
		#'select_module':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
		'select_module':fields.many2one('temp.module', 'Module'),
		'select_module2':fields.integer('Module2'),
		
		'class_name':fields.char('Class Name', readonly=1),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly=1),
		'end_date':fields.date('End Date', readonly=1),
		#'sch_date':fields.selection((_onchange_populate_schedule), 'Select Date', type='char'),
		'sch_date':fields.many2one('class.start.date', 'Select Date'),
		'sch_date2':fields.char('Select Date2'),
		#payment
		'payment_learner':fields.one2many('payment.module', 'pay_id','Payment Module', readonly=1),
		'payment_test_learner':fields.one2many('payment.test', 'pay_id','Payment Test', readonly=1),
		'Grand_total':fields.function(_amount, 'Grand Total', readonly=1),
		'Grand_test_total':fields.function(_amount_test, 'Grand Total', readonly=1),
		#Personal Tab Fields
		'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
		'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		#Education
		'high_qualification':fields.selection((('No Formal Qualification & Lower Primary','No Formal Qualification & Lower Primary'),('Primary PSLE','Primary PSLE'),('Lower Secondary','Lower Secondary'),('N Level or equivalent','N Level or equivalent'),
		('O Level or equivalent','O Level or equivalent'),('A Level or equivalent','A Level or equivalent'),('ITE Skills Certification (ISC)','ITE Skills Certification (ISC)'),('Higher NITEC','Higher NITEC'),('NITEC/Post Nitec','NITEC/Post Nitec'),
		('Polytechnic Diploma','Polytechnic Diploma'),('WSQ Diploma','WSQ Diploma'),('Professional Qualification & Other Diploma','Professional Qualification & Other Diploma'),('University First Degree','University First Degree'),
		('University Post-graduate Diploma & Degree/Master/Doctorate','University Post-graduate Diploma & Degree/Master/Doctorate'),('WSQ Certificate','WSQ Certificate'),('WSQ Higher Certificate','WSQ Higher Certificate'),('WSQ Advance Certificate','WSQ Advance Certificate'),
		('WSQ Diploma','WSQ Diploma'),('WSQ Specialist Diploma','WSQ Specialist Diploma'),('WSQ Graduate Diploma','WSQ Graduate Diploma'),('Others','Others'),('Not Reported','Not Reported')),'Highest Qualification'),
		'language_proficiency':fields.boolean('Language Proficiency'),
		#Contact
		'email_id': fields.char('Email'),
		'addr_1': fields.char('Address Line 1'),
		'addr_2': fields.char('Address Line 2'),
		'postal_code': fields.char('Postal Code', size=6),
		'mobile_no': fields.integer('Mobile Number', size=9),
		'landline_no': fields.integer('Home Number', size=9),
		'office_no': fields.integer('Office', size=9),
		#Modules
		'learner_mod_line': fields.one2many('learner.mode.line', 'qualification_module_id_1', 'Order Lines', select=True),
		'learner_mod_line_2': fields.one2many('learner.mode.line', 'qualification_module_id_2', 'Order Lines', select=True),
		'learner_mod_line_3': fields.one2many('learner.mode.line', 'qualification_module_id_3', 'Order Lines', select=True),
		'learner_mod_line_4': fields.one2many('learner.mode.line', 'qualification_module_id_4', 'Order Lines', select=True),
		'learner_mod_line_5': fields.one2many('learner.mode.line', 'qualification_module_id_5', 'Order Lines', select=True),
		'learner_mod_line_6': fields.one2many('learner.mode.line', 'qualification_module_id_6', 'Order Lines', select=True),
		# Module No.
		'no_module_box1': fields.boolean('1'),
		'no_module_box2': fields.boolean('2'),
		'no_module_box3': fields.boolean('3'),
		'no_module_box4': fields.boolean('4'),
		'no_module_box5': fields.boolean('5'),
		'no_module_box6': fields.boolean('6'),
		#1
		'mod_gp_name_1': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_1': fields.boolean('Select Group'),
		'set_group_as_sel_1': fields.boolean('Select Group'),
		'set_module_select_1': fields.boolean('Select'),
		'min_no_modules_1': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_1': fields.integer('Maximum Modules', readonly=1),
		#2
		'mod_gp_name_2': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_2': fields.boolean('Select Group'),
		'set_group_as_sel_2': fields.boolean('Select Group'),
		'set_module_select_2': fields.boolean('Select'),
		'min_no_modules_2': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_2': fields.integer('Maximum Modules', readonly=1),
		#3
		'mod_gp_name_3': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_3': fields.boolean('Select Group'),
		'set_group_as_sel_3': fields.boolean('Select Group'),
		'set_module_select_3': fields.boolean('Selectable'),
		'min_no_modules_3': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_3': fields.integer('Maximum Modules', readonly=1),
		#4
		'mod_gp_name_4': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_4': fields.boolean('Select Group'),
		'set_group_as_sel_4': fields.boolean('Select Group'),
		'set_module_select_4': fields.boolean('Selectable'),
		'min_no_modules_4': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_4': fields.integer('Maximum Modules', readonly=1),
		#5
		'mod_gp_name_5': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_5': fields.boolean('Select Group'),
		'set_group_as_sel_5': fields.boolean('Select Group'),
		'set_module_select_5': fields.boolean('Selectable'),
		'min_no_modules_5': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_5': fields.integer('Maximum Modules', readonly=1),
		#6
		'mod_gp_name_6': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_6': fields.boolean('Select Group'),
		'set_group_as_sel_6': fields.boolean('Select Group'),
		'set_module_select_6': fields.boolean('Selectable'),
		'min_no_modules_6': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_6': fields.integer('Maximum Modules', readonly=1),
		'outstanding_line': fields.one2many('outstanding.module','outstanding_id','outstanding'),
		'action_learn_line': fields.one2many('action.learn.module','action_id','Action'),
		'current_class_line': fields.one2many('current.class','class_id','Current Class', readonly=1),
		'class_history_line': fields.one2many('class.history.module','class_id','Class History', readonly=1),
		'test_history_line': fields.one2many('test.history.module', 'test_id', 'Test'),
		'test_score_line': fields.one2many('test.score.module','test_score_id','Test Scores',readonly=1),
		'qualification_line': fields.one2many('qualification.module','qualify_id','Qualification & Awards',readonly=1),
		'assets_line': fields.one2many('assets.learner.module','asset_id','Assets'),
		'feedback_line': fields.one2many('feedback.module','feedback_id','Feedback'),
		'remarks_line': fields.one2many('remarks.module','remarks_id','Remarks'),
		'race':fields.many2one('race', 'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'emp_staus': fields.many2one('employee.status', 'Employee Status'),
		'company_name':fields.many2one('company', 'Company'),
		'desig_detail':fields.many2one('designation', 'Designation'),
		'salary':fields.many2one('salary.range', 'Salary Range'),
		'sponsor_ship':fields.many2one('sponsership', 'Sponsership'),
		't_status':fields.char('Status'),
		'actual_number':fields.function(_calculate_total_checklist, relation="learner.info",readonly=1,string='No. Checklist',type='integer'),
		'status':fields.char('Status'),
		'apply_all':fields.boolean('Apply to All'),
	}
	
	_defaults = { 
	   'date1': fields.date.context_today,
	   'date2': fields.date.context_today,
	   'learner_status': 'Active',
	   'learner_nric': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'code'),
	   'nationality': 'Singapore',
	   'learner_id': 'default_learner_nric',
	   'status': 'Draft',
	}
	
	#_constraints = [(_mobile_no, 'Error: Mobile Number Cannot be Negative', ['Mobile']), (_landline_no, 'Error: Landline Number Cannot be Negative', ['Landline']), (_office_no, 'Error: Office Number Cannot be Negative', ['Office']), (_check_email, 'Error! Email is invalid.', ['work_email']),(_check_unique_id, 'Error: Email Already Exist', ['Email'])]

learner_profile_wizard()