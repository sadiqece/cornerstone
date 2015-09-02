from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

global dupliacte_program_found
dupliacte_program_found = False

global dupliacte_people_bu_found
dupliacte_people_bu_found = False

global dupliacte_people_bu_1_found
dupliacte_people_bu_1_found = False

###############

global dupliacte_program_found_create
dupliacte_program_found_create = False

global dupliacte_people_bu_found_create
dupliacte_people_bu_found_create = False

global dupliacte_people_bu_1_found_create
dupliacte_people_bu_1_found_create = False

class commisions(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(commisions, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
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
		
	def _check_unique_code(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.commision_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.commision_code and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.commision_code and self_obj.commision_code.lower() in  lst:
				return False
		return True
		
	def on_change_program_value(self, cr, uid, ids, program_line):
		if program_line == 0.00:
			raise osv.except_osv(_('Error!'),_("Duration - Cannot be negative value"))
		return {'value': {'pay_value': program_line}}
		
	def on_change_pay_value(self, cr, uid, ids, pay_value):
		val = {}
		val['pay_value_1'] = False
		val['pay_value_2'] = False		
		if pay_value == 'In $ (By Programs)':
			val['pay_value_1'] = True
		elif pay_value == 'In % (By Project Value)':
			val['pay_value_2'] = True
			
		return {'value': val}
		
	def _calculate_total_mod(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		#_logger.info('Adding rooms %s', mod_line_ids)
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = self.browse(cr, uid, line.id, context=context).people_bu_1 or self.browse(cr, uid, line.id, context=context).people_bu
			_logger.info('Adding rooms %s', mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
				
		return res
		
# Room mandatory
	def _make_mandatory1(self, cr, uid, ids, context=None):
			pl = self.pool.get('project.value.line')
			isFound = False
			for progline in self.browse(cr, uid, ids, context=None):
				if progline['pay_value'] == 'In % (By Project Value)':
					for line in progline.project_value_line:
						isFound = True
					if isFound:
						return True
					else:
						return False
			return True

	def _make_mandatory2(self, cr, uid, ids, context=None):
			pl = self.pool.get('project.value.line')
			isFound = False
			for progline in self.browse(cr, uid, ids, context=None):
				if progline['pay_value'] == 'In $ (By Programs)':
					for line in progline.program_line:
						isFound = True
					if isFound:
						return True
					else:
						return False
			return True

	_name = "commisions"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100, readonly=1),
		'commision_id': fields.char('Id',size=20),
		'name': fields.char('Commission Name', size=100,required=True, select=True),
		'commision_code': fields.char('Commission Code', size=20),
		'pay_value': fields.selection((('In $ (By Programs)','In $ (By Programs)'),('In % (By Project Value)','In % (By Project Value)')),'Pay Out Value', required=True),
		'pay_value_1': fields.boolean('Pay Out Value In $ (By Programs)'),
		'pay_value_2': fields.boolean('Pay Out Value In % In % (By Project Value)'),
		'program_line': fields.one2many('program.line', 'program_line_id', 'Program Lines'),
		'bussiness_id':fields.many2one('business', 'Applied To', ondelete='cascade', help='Bussiness', select=True),
		'date_added': fields.date('Date Added', readonly=1),
		'project_value_line': fields.one2many('project.value.line', 'project_value_lineid', 'Project Lines'),
		'people_bu': fields.one2many('people.bu', 'staff_line_id', 'People', select=True, required=True),
		'people_bu_1': fields.one2many('people.bu.one', 'staff_line1_id', 'People', select=True, required=True),
		'people_line': fields.one2many('people.line', 'people_business_id', 'People Lines', select=True, required=True),
		'applied_to': fields.function(_calculate_total_mod, relation="people.bu.one",readonly=1,string='Applied To',type='integer'),
		#'people_count': fields.function(_calculate_total_mod, relation="business",readonly=1,string='People Count',type='integer'),
		'commision_status': fields.selection((('Incomplete','Incomplete'),('Active','Active'),('InActive','InActive'),('Completed','Completed')),'Status', select=True),
	}
	
	_defaults = { 
	   'date_added': fields.date.context_today,
	   'commision_status': 'Active',
	  }
	  
	def create(self,cr, uid, values, context=None):
		
		global dupliacte_program_found_create
		dupliacte_program_found_create = False

		global dupliacte_people_bu_found_create
		dupliacte_people_bu_found_create = False

		global dupliacte_people_bu_1_found_create
		dupliacte_people_bu_1_found_create = False
		
		if 'program_line' in values :
			if values['program_line']  > 1:
				ids_test_lear = self.pool.get('program.line').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('program.line').browse(cr,1,ids_test_lear):
					if dd.program_line_id.id == True:
						table_ids.append(dd.program_id.id)	
				for x in values['program_line'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('program.line').browse(cr,uid,x[1])
						deleted_ids.append(obj.program_id.id)
					elif x[0] == 0 and 'program_id' in x[2]:
						added_ids.append(x[2]['program_id'])
						if x[2]['program_id'] in table_ids :
							new_table_ids.append(dd.program_id.id)
					elif x[0] == 1  and 'program_id' in x[2]:
						updated_ids.append(x[2]['program_id'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_program_found_create
					dupliacte_program_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_program_found_create
							dupliacte_program_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_program_found_create
						dupliacte_program_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_program_found_create
							dupliacte_program_found_create = True
							
		if 'people_bu' in values :
			if values['people_bu']  > 1:
				ids_test_lear = self.pool.get('people.bu').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('people.bu').browse(cr,1,ids_test_lear):
					if dd.staff_line_id.id == True:
						table_ids.append(dd.p_line_id.id)	
				for x in values['people_bu'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('people.bu').browse(cr,uid,x[1])
						deleted_ids.append(obj.p_line_id.id)
					elif x[0] == 0 and 'p_line_id' in x[2]:
						added_ids.append(x[2]['p_line_id'])
						if x[2]['p_line_id'] in table_ids :
							new_table_ids.append(dd.p_line_id.id)
					elif x[0] == 1  and 'p_line_id' in x[2]:
						updated_ids.append(x[2]['p_line_id'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_people_bu_found_create
					dupliacte_people_bu_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_people_bu_found_create
							dupliacte_people_bu_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_people_bu_found_create
						dupliacte_people_bu_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_people_bu_found_create
							dupliacte_people_bu_found_create = True
							
		if 'people_bu_1' in values :
			if values['people_bu_1']  > 1:
				ids_test_lear = self.pool.get('people.bu.one').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('people.bu.one').browse(cr,1,ids_test_lear):
					if dd.staff_line1_id.id == True:
						table_ids.append(dd.p_line1_id.id)	
				for x in values['people_bu_1'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('people.bu.one').browse(cr,uid,x[1])
						deleted_ids.append(obj.p_line1_id.id)
					elif x[0] == 0 and 'p_line1_id' in x[2]:
						added_ids.append(x[2]['p_line1_id'])
						if x[2]['p_line1_id'] in table_ids :
							new_table_ids.append(dd.p_line1_id.id)
					elif x[0] == 1  and 'p_line1_id' in x[2]:
						updated_ids.append(x[2]['p_line1_id'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_people_bu_1_found_create
					dupliacte_people_bu_1_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_people_bu_1_found_create
							dupliacte_people_bu_1_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_people_bu_1_found_create
						dupliacte_people_bu_1_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_people_bu_1_found_create
							dupliacte_people_bu_1_found_create = True
	
		module_id = super(commisions, self).create(cr, uid, values, context=context)
		return module_id
	  
	def write(self,cr, uid, ids, values, context=None):
	
		global dupliacte_program_found
		dupliacte_program_found = False
		
		global dupliacte_people_bu_found
		dupliacte_people_bu_found = False
		
		global dupliacte_people_bu_1_found
		dupliacte_people_bu_1_found = False
	
		if 'program_line' in values :
				if values['program_line']  > 1:
					ids_test_lear = self.pool.get('program.line').search(cr,1,[])
					table_ids = [] 
					added_ids = []
					deleted_ids =[]
					updated_ids = []
					for dd in self.pool.get('program.line').browse(cr,1,ids_test_lear):
						if dd.program_line_id.id == ids[0]:
							table_ids.append(dd.program_id.id)
					for x in values['program_line'] :
						if x[0] == 2 and x[2] ==  False :
							obj = self.pool.get('program.line').browse(cr,uid,x[1])
							deleted_ids.append(obj.program_id.id)
						elif x[0] == 0 and 'program_id' in x[2]:
							added_ids.append(x[2]['program_id'])
						elif x[0] == 1  and 'program_id' in x[2]:
							updated_ids.append(x[2]['program_id'])
					'''create check'''		
					if len(added_ids) - len(set(added_ids)) >  0 :
						global dupliacte_program_found
						dupliacte_program_found = True
					else:
						'''check create in table'''
						for c in added_ids :
							if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
								global dupliacte_program_found
								dupliacte_program_found = True
						'''check for update ids '''
						if len(updated_ids) - len(set(updated_ids)) >  0 :
							global dupliacte_program_found
							dupliacte_program_found = True
						else :
							found = 0
							for u in updated_ids :
								if u in table_ids and  u not in deleted_ids :
									found = found +1
							if found == 1 :
								global dupliacte_program_found
								dupliacte_program_found = True
		if 'people_bu' in values :
				if values['people_bu']  > 1:
					ids_test_lear = self.pool.get('people.bu').search(cr,1,[])
					table_ids = [] 
					added_ids = []
					deleted_ids =[]
					updated_ids = []
					for dd in self.pool.get('people.bu').browse(cr,1,ids_test_lear):
						if dd.staff_line_id.id == ids[0]:
							table_ids.append(dd.p_line_id.id)
					for x in values['people_bu'] :
						if x[0] == 2 and x[2] ==  False :
							obj = self.pool.get('people.bu').browse(cr,uid,x[1])
							deleted_ids.append(obj.p_line_id.id)
						elif x[0] == 0 and 'p_line_id' in x[2]:
							added_ids.append(x[2]['p_line_id'])
						elif x[0] == 1  and 'p_line_id' in x[2]:
							updated_ids.append(x[2]['p_line_id'])
					'''create check'''		
					if len(added_ids) - len(set(added_ids)) >  0 :
						global dupliacte_people_bu_found
						dupliacte_people_bu_found = True
					else:
						'''check create in table'''
						for c in added_ids :
							if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
								global dupliacte_people_bu_found
								dupliacte_people_bu_found = True
						'''check for update ids '''
						if len(updated_ids) - len(set(updated_ids)) >  0 :
							global dupliacte_people_bu_found
							dupliacte_people_bu_found = True
						else :
							found = 0
							for u in updated_ids :
								if u in table_ids and  u not in deleted_ids :
									found = found +1
							if found == 1 :
								global dupliacte_people_bu_found
								dupliacte_people_bu_found = True
								
		if 'people_bu_1' in values :
				if values['people_bu_1']  > 1:
					ids_test_lear = self.pool.get('people.bu.one').search(cr,1,[])
					table_ids = [] 
					added_ids = []
					deleted_ids =[]
					updated_ids = []
					for dd in self.pool.get('people.bu.one').browse(cr,1,ids_test_lear):
						if dd.staff_line1_id.id == ids[0]:
							table_ids.append(dd.p_line1_id.id)
					for x in values['people_bu_1'] :
						if x[0] == 2 and x[2] ==  False :
							obj = self.pool.get('people.bu.one').browse(cr,uid,x[1])
							deleted_ids.append(obj.p_line1_id.id)
						elif x[0] == 0 and 'p_line1_id' in x[2]:
							added_ids.append(x[2]['p_line1_id'])
						elif x[0] == 1  and 'p_line1_id' in x[2]:
							updated_ids.append(x[2]['p_line1_id'])
					'''create check'''		
					if len(added_ids) - len(set(added_ids)) >  0 :
						global dupliacte_people_bu_1_found
						dupliacte_people_bu_1_found = True
					else:
						'''check create in table'''
						for c in added_ids :
							if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
								global dupliacte_people_bu_1_found
								dupliacte_people_bu_1_found = True
						'''check for update ids '''
						if len(updated_ids) - len(set(updated_ids)) >  0 :
							global dupliacte_people_bu_1_found
							dupliacte_people_bu_1_found = True
						else :
							found = 0
							for u in updated_ids :
								if u in table_ids and  u not in deleted_ids :
									found = found +1
							if found == 1 :
								global dupliacte_people_bu_1_found
								dupliacte_people_bu_1_found = True
								
		module_id = super(commisions, self).write(cr, uid, ids,values, context=context)
		return module_id
	
	def on_change_bussiness_id(self, cr, uid, ids, bussiness_id):
		bussiness_obj = self.pool.get('business').browse(cr, uid, bussiness_id)
		return {'value': {'s_no': bussiness_obj.s_no, 'name': bussiness_obj.name,'business_code':bussiness_obj.business_code,'unit_line':bussiness_obj.unit_line}}
	
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'bussiness_form')
		view_id = view_ref and view_ref[1] or False
		loc_room_obj = self.pool.get('business')
		loc_room_ids = loc_room_obj.search(cr, uid, [('id', '=', ids[0])])
		room_ids =[]
		for loc_room_line in loc_room_obj.browse(cr, uid, loc_room_ids,context=context):
			room_ids.append(loc_room_line['bussiness_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'name': _('Bussiness'),
		'res_model': 'bussiness',
		'view_type': 'form',
		'res_id': room_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}
		
	_constraints = [(_check_unique_name, 'Error: Commission Name Already Exists', ['Name']),(_check_unique_code, 'Error: Commission Code Already Exists', ['Commission Code']),(_make_mandatory1, 'Error: Create Atleast One Schedule', ['Schedule']),(_make_mandatory2, 'Error: Select Atleast One Program', ['Program'])]
commisions

class program_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(program_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

# Zeya 7-1-15		

	def _check_commvalue(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.value < 0:
				return False
		return True

	def _check_unique_module(self, cr, uid, ids, context=None):
		if dupliacte_program_found == True:
			return False
		if dupliacte_program_found_create == True:
			return False
		else :
			return True
		
# EOF		

	_name = "program.line"
	_description = "Module Line"
	_columns = {
		's_no': fields.integer('S.No', size=3, readonly=1),
		'program_line_id': fields.many2one('commisions', 'Commissions', ondelete='cascade', help='Commissions', select=True),
		'program_id':fields.many2one('lis.program', 'Program Name', ondelete='cascade', help='Program', select=True, required=True),
		'program_code': fields.related('program_id','program_code',type="char",relation="lis.program",string="Program Code", readonly=1),
		'value': fields.integer('Value',size=6),
	}
	_constraints = [(_check_unique_module, 'Error: Program Already Exists', ['Program Name']),(_check_commvalue, 'Error: Value Cannot be negative', ['Value'])]
program_line

class project_value_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(project_value_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res
		
	def _check_value1(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.value1 < 0:
				return False
		return True
		
	def _check_min_max_srange(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.s_range1 < 0 or self_obj.e_range1 < 0 or self_obj.s_range1 > self_obj.e_range1:
				return False
		return True
# 19-1-15	

# Zeya 19-1-15
	'''def ranges_between(self, s_range1, e_range1):
		 latest_start = max(r1.s_range1, r2.s_range1)
		 earliest_end = min(r1.e_range1, r2.e_range1)
		 overlap = (earliest_e_range1 - latest_s_range1).val + 1
		 overlap
		return r.val
'''
	def _check_all_range(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, uid ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.project_value_lineid == self_obj.project_value_lineid and x.e_range1 == self_obj.e_range1:
						return False
					elif x.project_value_lineid == self_obj.project_value_lineid and self_obj.s_range1 >= x.s_range1 and self_obj.s_range1 <= x.e_range1:
						return False
					elif x.project_value_lineid == self_obj.project_value_lineid and self_obj.e_range1 >= x.s_range1 and self_obj.e_range1 <= x.e_range1:
						return False
		return True

		
	_name = "project.value.line"
	_description = "Project Line"
	_columns = {
		'sr_no': fields.integer('S.No', size=100, readonly=1),
		's_range1':fields.integer('Start of Range',size=6,required=True),
		'e_range1': fields.integer('End of Range',size=6, required=True),
		'value1': fields.integer('Value',size=3, required=True),
		'project_value_lineid': fields.many2one('commisions', 'Commissions', ondelete='cascade', help='Commissions', select=True),
	}
	_defaults = { 
	   's_range1': 0,
	   'e_range1': 0,
	   'value1': 0,
	  }
	_constraints = [(_check_value1, 'Error: Value Cannot be negative', ['Value']),(_check_min_max_srange, 'Error: Start and End Range values are not correct', ['Range']),(_check_all_range, 'Error: Start or End Range Values Already Exist', ['Check Start or End Range'])]

	def onchange_range(self, cr, uid, ids, sr, er, context=None):
		res = {'value':{}}
		'''for line in self.browse(cr, uid, ids, ):
			#raise osv.except_osv(_('Warning!'),_('not %s')%(line.count))
			if sr >= line.s_range1 and sr <= line.e_range1:
				res['value']['s_range1'] = ''
				#raise osv.except_osv(_('Warning!'),_('not %s %s')%(line.s_range1, line.e_range1))
				res.update({'warning': {'title': _('Warning !'), 'message': _('Range already exist.')}})
				return res
			#history_line_id = self.browse(cr, uid, ids[0], context=context).history_line or []
			return 1'''
		#ids = self.pool.get('project.value.line').search(cr, uid, [('s_range1', '>=', sr) and ('e_range1', '<=', sr) ], context=context)
		sql="select s_range1, e_range1 from project_value_line"
		cr.execute(sql);
		rec = cr.fetchall()
		for i in rec:
			#ids2 = self.pool.get('project.value.line').search(cr, uid, [('e_range1', '<=', sr) ], context=context)
			#if ids2:
			#raise osv.except_osv(_('Warning!'),_('not %s %s %s')%(i[0] , i[1], sr))
			if sr >= i[0] and sr <= i[1]:
				res['value']['s_range1'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Range already exist.')}})
				return res
			elif er >= i[0] and er <= i[1]:
				res['value']['e_range1'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Range already exist.')}})
				return res
		return 1
		'''p_obj = self.pool.get('project.value.line') 
		value_ids = p_obj.search(cr, uid, None, context=context)
		val2 ={}
		sub_lines = []
		for line in p_obj.browse(cr, uid, value_ids, context=context):
			raise osv.except_osv(_('Warning!'),_('ccc %s %s')%(line.s_range1, line.e_range1))
			#sub_lines.append({'outs_item':prog_line['master_show_do'].id, 'outs_confirmation':prog_line['supp_doc_req']})
		return 1'''
		
project_value_line

class people_bu(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(people_bu, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res
		
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.staff_line_id == self_obj.staff_line_id and x.p_line_id == self_obj.p_line_id:
						return False
		return True
		
	def on_change_people_id(self, cr, uid, ids, p_line_id):
		business_obj = self.pool.get('people.line').browse(cr, uid, p_line_id)
		_logger.info("Business name %s %s", business_obj, p_line_id) 
		return {'value': {'business_id': business_obj.people_business_id.name}}
		

	_name = "people.bu"
	_description = "People"
	_columns = {
		'sr_no': fields.integer('S.No', size=100, readonly=1),
		'staff_line_id': fields.many2one('commisions', 'Commissions', ondelete='cascade', help='Commissions', select=True),
		'p_line_id': fields.many2one('people.line', 'Staff', ondelete='cascade', help='Business Unit', select=True, required=True),
		'business_info': fields.related('p_line_id','people_business_id',type="many2one",relation="people.line", readonly=1),
		'business_id': fields.char('BU', readonly=1),
		'date_added': fields.date('Date Added', readonly=1),
	}
	_defaults = { 
	   'date_added': fields.date.context_today,
	  }
	_constraints = [(_check_unique_name, 'Error: Staff already exist', ['Staff'])]
people_bu

class people_bu_1(osv.osv):

	def on_change_people1_id(self, cr, uid, ids, p_line_id):
		business_obj = self.pool.get('people.line').browse(cr, uid, p_line_id)
		_logger.info("Business name %s %s", business_obj, p_line_id) 
		return {'value': {'bu_1': business_obj.people_business_id.name}}

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(people_bu_1, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res
		
	def _check_unique_name(self, cr, uid, ids, context=None):
		if dupliacte_people_bu_1_found == True:
			return False
		if dupliacte_people_bu_1_found_create == True:
			return False
		else :
			return True
		
	_name = "people.bu.one"
	_description = "People"
	_columns = {
		'sr_no': fields.integer('S.No', size=100, readonly=1),
		'staff_line1_id': fields.many2one('commisions', 'Commissions', ondelete='cascade', help='Commissions', select=True),
		'p_line1_id': fields.many2one('people.line', 'Staff', ondelete='cascade', help='Test', select=True, required=True),
		'business_info': fields.related('p_line1_id','people_business_id',type="many2one",relation="people.line", readonly=1),
		'bu_1': fields.char('BU', readonly=1),
		'date_added_1': fields.date('Date Added', readonly=1),
	}
	_defaults = { 
	   'date_added_1': fields.date.context_today,
	  }
	_constraints = [(_check_unique_name, 'Error: Staff already exist', ['Staff'])]
people_bu_1

