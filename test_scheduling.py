from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class test_listing_page_info(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(test_listing_page_info, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	_name = "test.listing.page.info"
	_description = "This table is for keeping Test Schedules"
	_columns = {
		's_no': fields.integer('S_No', size=100),
		'name': fields.char('Name', size=20),
		'test_name_id': fields.many2one('test', 'Test Name',  ondelete='cascade', help='Module', select=True, required=True),
		'test_definitation': fields.selection((('Pre Test','Pre Test'),('In Class Test','In Class Test'),('Post Test','Post Test')),'Test Definitions', required=True),
		'test_code': fields.char('Test Code', size=20, readonly=1),
		'test_code_compliance': fields.char('Test Code (Compliance)', size=20),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, required=True),
		'module_code': fields.char('Module Code', size=20, readonly=1),
		'start_date': fields.date('Start Date',readonly=1),
		'start_time': fields.float('Start Time'),
		'end_date': fields.date('End Date',readonly=1),
		'end_time': fields.float('End Time', size=3),
		'room_id':fields.many2one('room', 'Rooms', ondelete='cascade', help='Room', select=True, required=True),
		'test_modality': fields.one2many('test.modality','s_no', 'Test Modality'),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
		'learner': fields.one2many('learner','s_no','Learner'),
		'test_scores': fields.one2many('test.scores','s_no','Test Scores'),
		'status': fields.char('Status', size=20),
		'capacity': fields.char('Capacity', size=20),
		'actual_number': fields.char('Actual Number', size=20),
	}
	
	def on_change_test_name_id(self, cr, uid, ids, test_name_id):
		test_name_obj = self.pool.get('test').browse(cr, uid, test_name_id)
		return {'value': {'name': test_name_obj.name,'test_code':test_name_obj.test_code,'test_max_Pax':test_name_obj.test_max_Pax,'test_status':test_name_obj.test_status}}
	
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
		
	def on_change_room_id(self, cr, uid, ids, room_id):
		room_obj = self.pool.get('room').browse(cr, uid, room_id)
		return {'value': {'s_no': room_obj.s_no, 'room_floor_area': room_obj.room_floor_area,'room_setup':room_obj.room_setup,'room_max_cap':room_obj.room_max_cap}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'room_form')
		view_id = view_ref and view_ref[1] or False
		loc_room_obj = self.pool.get('location.room.line')
		loc_room_ids = loc_room_obj.search(cr, uid, [('id', '=', ids[0])])
		room_ids =[]
		for loc_room_line in loc_room_obj.browse(cr, uid, loc_room_ids,context=context):
			room_ids.append(loc_room_line['room_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'name': _('Room'),
		'res_model': 'room',
		'view_type': 'form',
		'res_id': room_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}
		
	_defaults = { 
	   'start_date': fields.date.context_today,
	}
	
test_listing_page_info()

class test_modality(osv.osv):
	_name ='test.modality'
	_description ="Trainer Learner Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'test_id':fields.many2one('master.modalities', 'Test Modality', ondelete='cascade', help='Test', select=True, required=True),
	'active':fields.boolean('Active'),
	}
	
	def on_change_test_id(self, cr, uid, ids, test_id):
		test_obj = self.pool.get('master.modalities').browse(cr, uid, test_id)
		return {'value': {'name': test_obj.name, 'level': test_obj.level,'store_results':test_obj.store_results}}
	
test_modality()

class learner(osv.osv):
	_name ='learner'
	_description ="Learner Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'name':fields.char('Name',size=25, required=True),
	'nric_fin':fields.char('NRIC/FIN',size=25, required=True),
	'class_code':fields.char('Class Code',size=25, required=True),
	'compliance_code':fields.char('Compliance Code',size=25, required=True),
	'level':fields.char('Level',size=25, required=True),
	'attendance':fields.char('Attendance',size=25, required=True),
	'reading':fields.boolean('Reading'),
	'listening':fields.boolean('Listening'),
	'speaking':fields.boolean('Speaking'),
	'writing':fields.boolean('Writing'),
	'numeracy':fields.boolean('Numeracy'),
	}
learner()

class test_scores(osv.osv):
	_name ='test.scores'
	_description ="Test Scores Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'name':fields.char('Name',size=25, required=True),
	'nric_fin':fields.char('NRIC/FIN',size=25, required=True),
	'compr':fields.char('Compr',size=25),
	'conv':fields.char('Conv',size=25),
	'r_level':fields.integer('R(Level)',size=1),
	'r_scores':fields.integer('R(Scores)',size=2),
	'l_level':fields.integer('L(Level)',size=1),
	'l_scores':fields.integer('L(Scores)',size=2),
	's_level':fields.integer('S(Level)',size=1),
	's_scores':fields.integer('S(Soures)',size=2),
	'w_level':fields.integer('W(Level)',size=1),
	'w_scores':fields.integer('W(Scores)',size=2),
	'w_outcome':fields.char('W(Outcomes)',size=20),
	'n_level':fields.integer('N(Level)',size=1),
	'n_scores':fields.integer('N(Scores)',size=2),
	'n_outcome':fields.char('N(Outcomes)',size=20),
	}
test_scores()