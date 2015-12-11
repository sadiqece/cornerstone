import datetime
from dateutil import relativedelta
from openerp import addons
import logging
import time
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
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
		today = datetime.date.today()
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		sub_lines.append( (0,0, {'date_created':today.strftime('%d-%m-%Y'),'created_by':current_user['name'],
			'last_update':'-','last_update_by':'-','date_status_change':today.strftime('%d-%m-%Y'),'status_change_by':current_user['name']}) )
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
		test_list ={'name': 'Test Name','test_code': 'Test Code','modality_line':'Modalities','history_line': 'History', 'delivery_mode': 'Delivery Mode' }
		arr={}
		for i in range(len(changes)):
			if changes[i] in test_list:
				arr[i] = test_list[changes[i]]
		today = datetime.date.today()  
		sub_lines.append( (0,0, {'date_created':history_line_id[0]['date_created'],'created_by':history_line_id[0]['created_by'],
			'last_update':today.strftime('%d-%m-%Y'),'last_update_by':current_user['name'],'date_status_change':staus_changed_date,'status_change_by':staus_changed_by,'changes':arr.values()}) )
		values.update({'history_line': sub_lines})
		name = super(test, self).write(cr, uid, ids,values, context=context)
		return name
		
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
		'test_status': fields.selection((('Active','Active'),('InActive','InActive')),'Status'),
		'modality_line': fields.one2many('modalities.module','modality_id','Modalities'),
		'history_line': fields.one2many('test.history','test_id','History', limit=None),
		'test_type': fields.char('Test Type'),
		'modules_applied': fields.function(_modules_applied, 'Modules Applied', type="one2many"),
	}
	_defaults = {
		'test_status': 'Active'
	}
	_constraints = [(_check_unique_name, 'Error: Test Name Already Exists', ['Name']),(_check_unique_code, 'Error: Test Code Already Exists', ['Test Code'])]
test()

class modalities(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(modalities, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	'''def _check_level(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.level < 0:
				return False
		return True	'''	
		
	def _check_unique_test(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.modality_id == self_obj.modality_id and x.modality == self_obj.modality:
						return False
		return True
		
	def on_change_master_modality(self, cr, uid, ids, module_modality):
		if not module_modality: return {}
		master_modalities_obj = self.pool.get('master.modality').browse(cr, uid, module_modality)
		return {'value': {'name': master_modalities_obj.name,'cost':master_modalities_obj.cost}}
		
	_name ='modalities.module'
	_description ="Modalities Tab"
	_columns = {
	'modality_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'modality':fields.many2one('master.modality', 'Test Modality', ondelete='cascade', help='Description', required=True),
	'cost': fields.float('Cost($)', size=7, readonly=1),
	#'level':fields.integer('Minimum Level',size=1),
	'store_results':fields.boolean('Store Result'),
	'store_level':fields.boolean('Store Level'),
	'store_scores':fields.boolean('Store Scores'),
	'store_outcome':fields.boolean('Store Outcome'),
	}
	_constraints = [(_check_unique_test, 'Error: Test Modality Already Exists', ['Name'])]
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
test_history()

#Class Module Master Test
###############
class master_modality(osv.osv):
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
	_name ='master.modality'
	_description ="Modality"
	_columns = {
	'name':fields.char('Modality',size=20),
	'cost': fields.float('Cost', size=7),
	}
	_constraints = [(_check_unique_name, 'Error: This Modality Already Exists', ['name'])]
master_modality()

	