from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class test(osv.osv):
	_name = "test"
	_description = "This table is for keeping test data"
	_columns = {
		'location_id': fields.char('Id',size=20),
		'name': fields.char('Test Name', size=100,required=True, select=True),
		'test_code': fields.char('Test Code', size=20),
		'test_fee': fields.float('Test Fee', size=4),
		'test_max_Pax':fields.integer('Max Pppl', size=4),
		'test_status': fields.selection((('Active','Active'),('InActive','InActive')),'Status'),
		'test_description': fields.text('Description'),
		'test_mod_line': fields.one2many('test.module.line', 'test_mod_id', 'Order Lines', select=True, required=True),
		'modality_line': fields.one2many('modalities.module','modality_id','Modalities'),
		'history_line': fields.one2many('test.history','test_id','History', limit=None),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
	}
test()

class test_mod_line(osv.osv):
	def _check_unique_module(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.test_mod_id == self_obj.test_mod_id and x.module_id == self_obj.module_id:
						return False
		return True
		
	def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
		res = super(cs_module,self).fields_view_get(cr, user, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
		doc = etree.XML(res['arch'])

		global globvar
		if globvar == 1:
			for node in doc.xpath("//div[@id='div_status1']"):
				node.set('class', "view_red")
			for node in doc.xpath("//div[@id='div_status2']"):
				node.set('class', "view_green")
			globvar = 0
			res['arch'] = etree.tostring(doc)
			return res	
	
	
	_name = "test.module.line"
	_description = "Module Line"
	_columns = {
		'test_mod_id': fields.many2one('test', 'Test', ondelete='cascade', help='Test', select=True),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
		'module_code': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'pre_test': fields.boolean('Pre Test'),
		'inclass_test': fields.boolean('In Class Test'),
		'post_test': fields.boolean('Post Test'),
	}
	_constraints = [(_check_unique_module, 'Error: Module Already Exists', ['module_id'])]
	
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
	
test_mod_line()


class modalities(osv.osv):
	_name ='modalities.module'
	_description ="Modalities Tab"
	_columns = {
	'modality_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'modal_list':fields.many2one('master.modalities', 'Test Modality', ondelete='cascade', help='Description', select=True,required=True),
	'level':fields.char('Minimum Level',size=3),
	'store_results':fields.boolean('Store Result'),
	'store_level':fields.boolean('Store Level'),
	'store_scores':fields.boolean('Store Scores'),
	'store_outcome':fields.boolean('Store Outcome'),
	}
	
	
modalities	()

class master_modalities(osv.osv):
	_name ='master.modalities'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Test Descripton',size=20),
	'level':fields.char('Minimum Level',size=3),
	'store_results':fields.boolean('Store Result'),
	}
master_modalities()


class test_history(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(history, self).read(cr, uid,ids, fields, context, load)
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


	