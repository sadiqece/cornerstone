import datetime
from dateutil import relativedelta
from openerp import addons
import logging
import time
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from datetime import datetime
import re

_logger = logging.getLogger(__name__)

class test(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(test, self).read(cr, uid,ids, fields, context, load)
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
				x.test_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.test_code and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.test_code and self_obj.test_code.lower() in  lst:
				return False
		return True
		
	def create(self,cr, uid, values, context=None):
		sub_lines = []
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		sub_lines.append( (0,0, {'date_created':fields.date.today(),'created_by':current_user['name'],
			'last_update':'-','last_update_by':'-','date_status_change':fields.date.today(),'status_change_by':current_user['name']}) )
		values.update({'history_line': sub_lines})
		name = super(test, self).create(cr, uid, values, context=context)
		return name
		
	def write(self,cr, uid, ids, values, context=None):
		sub_lines = []
		
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		for line in self.browse(cr, uid, ids, context=context):
			history_line_id = self.browse(cr, uid, ids[0], context=context).history_line or []

		num_of_his = len(history_line_id)-1 
		staus_changed_by =   history_line_id[num_of_his]['status_change_by']
		staus_changed_date =   history_line_id[num_of_his]['date_status_change']
 
		if 'test_status' in values:
			staus_changed_date = fields.date.today()
			staus_changed_by  = current_user['name']

		changes = values.keys()
		test_list ={'name': 'Test Name','test_code': 'Test Code','test_fee':'Test Fee','test_max_Pax':'Max Pppl',
				'test_status': 'Status','test_description': 'Description','modality_line':'Modalities','history_line': 'History', 'delivery_mode': 'Delivery Mode' }
		arr={}
		for i in range(len(changes)):
			if changes[i] in test_list:
				arr[i] = test_list[changes[i]]
  
		sub_lines.append( (0,0, {'date_created':history_line_id[0]['date_created'],'created_by':history_line_id[0]['created_by'],
			'last_update':fields.date.today(),'last_update_by':current_user['name'],'date_status_change':staus_changed_date,'status_change_by':staus_changed_by,'changes':arr.values()}) )
		values.update({'history_line': sub_lines})
		name = super(test, self).write(cr, uid, ids,values, context=context)
		return name
		
	'''def _modules_applied(self, cr, uid, ids, field_names, args,  context=None):
		modules_applied = self.pool.get('test.module.line')
		test = modules_applied.browse(cr, uid, ids[0],context=context)
		module_mod_ids = modules_applied.search(cr, uid, [('test_mod_id', '=', ids[0])])
		module_ids =[]
		res = {}
		for prog_module_line in modules_applied.browse(cr, uid, module_mod_ids,context=context):
			module_ids.append(prog_module_line['test_mod_id'].id)
		return res'''
		
	def _modules_applied(self, cr, uid, ids, module_id, args,  context=None):
		modules_applied = self.pool.get('test.module.line').browse(cr, uid, module_id)
		return {'value': {'module_code': modules_applied.module_code}}
		
#Validate for test fee		
	def _check_test_fee(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.test_fee < 0:
				return False
		return True
		
#Validate Max of People	
	def _check_test_max_Pax(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.test_max_Pax < 0:
				return False
		return True		
		
	'''def on_change_test_type(self, cr, uid, ids,pre_test, in_class_test, post_test):
		test_type = 0
		if pre_test :
			test_type=1
		if in_class_test :
			test_type=1
		if post_test :
			test_type=1	
		return {'value': {'test_type': test_type}}'''	

	def views_test(self, cr, uid, ids, context=None):  
		this = self.browse(cr, uid, ids, context=context)[0]  
		mod_obj = self.pool.get('ir.model.data')  
		res = mod_obj.get_object_reference(cr, uid, 'cornerstone', 'test_form')  
		return {  
			'type': 'ir.actions.act_window',  
			'name': 'ESIC',  
			'view_type': 'form',  
			'view_mode': 'tree,form',  
			'view_id': False,  
			'res_model': 'test.module.line',  
			'nodestroy': True,  
			'res_id': False, # assuming the many2one is (mis)named 'hr_esic'  
			'target': 'current',  
			'context':{},  
			'flags': {'form': {'action_buttons': True}}  
			#'views': [(True, 'form')],  
		}
		
	_name = "test"
	_description = "This table is for keeping test data"
	_columns = {
		's_no': fields.integer('S.No',size=3),
		'name': fields.char('Test Name', size=100,required=True, select=True),
		'test_code': fields.char('Test Code', size=20),
		'test_fee': fields.float('Test Fee', size=6),
		'test_max_Pax':fields.integer('Max Pppl', size=4),
		'test_status': fields.selection((('Active','Active'),('InActive','InActive')),'Status'),
		'test_description': fields.text('Description'),
		#'test_modules': fields.many2one('test.module.line', ondelete='cascade', help='Module', select=True, required=True),
		#'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
		'test_mod_line': fields.one2many('test.module.line', 'test_mod_id', 'Order Lines', required=True),
		'modality_line': fields.one2many('modalities.module','modality_id','Modalities'),
		'history_line': fields.one2many('test.history','test_id','History', limit=None),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
		'test_type': fields.char('Test Type'),
		'modules_applied': fields.function(_modules_applied, 'Modules Applied', type="one2many"),
	}
	_defaults = {
		'test_status': 'Active'
	}
	_constraints = [(_check_test_fee, 'Error: Test Fee Cannot be Negative', ['Test Fee']),(_check_test_max_Pax, 'Error: Max Pppl Cannot be Negative', ['Max People']),
	(_check_unique_name, 'Error: Test Name Already Exists', ['Name']),(_check_unique_code, 'Error: Test Code Already Exists', ['Test Code'])]
test()

class test_mod_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(test_mod_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	def _check_unique_module(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.test_mod_id == self_obj.test_mod_id and x.module_id == self_obj.module_id:
						return False
		return True	
	
	_name = "test.module.line"
	_description = "Module Line"
	_columns = {
		's_no' : fields.integer('S.No',size=20,readonly=1),
		'test_mod_id': fields.many2one('test', 'Test', ondelete='cascade', help='Test', select=True),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
		'module_code': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'pre_test': fields.boolean('Pre Test'),
		'in_class_test': fields.boolean('In Test'),
		'post_test': fields.boolean('Post Test'),
	}
	_constraints = [(_check_unique_module, 'Error: Module Already Exists', ['Module'])]
	
	def on_change_module_id(self, cr, uid, ids, module_id):
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		return {'value': {'module_code': module_obj.module_code}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('test.module.line')
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
	
test_mod_line()


class modalities(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(modalities, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _check_level(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.level < 0:
				return False
		return True		
		
	def _check_unique_test(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.modality_id == self_obj.modality_id and x.modal_list == self_obj.modal_list:
						return False
		return True
		
	_name ='modalities.module'
	_description ="Modalities Tab"
	_columns = {
	'modality_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'modal_list':fields.many2one('master.modalities', 'Test Modality', ondelete='cascade', help='Description', select=True,required=True),
	'level':fields.integer('Minimum Level',size=3),
	'store_results':fields.boolean('Store Result'),
	'store_level':fields.boolean('Store Level'),
	'store_scores':fields.boolean('Store Scores'),
	'store_outcome':fields.boolean('Store Outcome'),
	}
	_constraints = [(_check_level, 'Error: Minimum Level Cannot be negative', ['Level']),(_check_unique_test, 'Error: Test Modality Already Exists', ['Name'])]
modalities	()

class master_modalities(osv.osv):
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
	_name ='master.modalities'
	_description ="People and Facilites Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'name':fields.char('Test Descripton',size=20),
	}
	_constraints = [(_check_unique_name, 'Error: Test Modality Already Exists', ['Name'])]
master_modalities()


class test_history(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(test_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='test.history'
	_description ="History Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'history_id':fields.integer('Id',size=20),
	'date_created':fields.char('Date Created',size=20),
	'created_by':fields.char('Created By',size=20),
	'last_update':fields.char('Last Update',size=20),
	'last_update_by':fields.char('Last Update By',size=20),
	'date_status_change':fields.char('Date Of Status Change',size=20),
	'status_change_by':fields.char('Status Change By',size=20),
	'changes':fields.char('Changes',size=200),
	'test_id': fields.many2one('test', 'Test', ondelete='cascade', help='Test', select=True),
	}
test_history	()


	