from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

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
		if pay_value == 'In $':
			val['pay_value_1'] = True
		elif pay_value == 'In %':
			val['pay_value_2'] = True
			
		return {'value': val}

	_name = "commisions"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100, readonly=1),
		'commision_id': fields.char('Id',size=20),
		'name': fields.char('Commisions Name', size=100,required=True, select=True),
		'commision_code': fields.char('Commisions Code', size=20),
		'pay_value': fields.selection((('In $','In $'),('In %','In %')),'Pay Out Value'),
		'pay_value_1': fields.boolean('Pay Out Value In $'),
		'pay_value_2': fields.boolean('Pay Out Value In %'),
		'program_line': fields.one2many('program.line', 'program_line_id', 'Program Lines', select=True, required=True),
		'bussiness_id':fields.many2one('business', 'Applied To', ondelete='cascade', help='Bussiness', select=True),
		'applied_to': fields.integer('Applied To',size=10),
		'date_added': fields.date('Date Added'),
		'project_value_line': fields.one2many('project.value.line', 'project_value_line_id', 'Project Lines', select=True, required=True),
	}
	
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
		
	_constraints = [(_check_unique_name, 'Error: Commisions Name Already Exists', ['name']),(_check_unique_code, 'Error: Commisions Code Already Exists', ['commision_code'])]
commisions

class program_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(program_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.program_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.program_code and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.program_code and self_obj.program_code.lower() in  lst:
				return False
		return True
		

	_name = "program.line"
	_description = "Module Line"
	_columns = {
		's_no': fields.integer('S.No', size=100, readonly=1),
		'program_line_id': fields.many2one('commisions', 'Commisions', ondelete='cascade', help='Commisions', select=True),
		'program_id':fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True, required=True),
		'program_code': fields.related('program_id','program_code',type="char",relation="lis.program",string="Program Code", readonly=1),
		'value': fields.char('Value',size=6),
	}
	_constraints = [(_check_unique_name, 'Error: Program Label Already Exists', ['program_code'])]
program_line

class project_value_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(project_value_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res
		
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.s_range1.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.s_range1 and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.s_range1 and self_obj.s_range1.lower() in  lst:
				return False
		return True
		
	_name = "project.value.line"
	_description = "Project Line"
	_columns = {
		'sr_no': fields.integer('S.No', size=100, readonly=1),
		'project_value_line_id': fields.many2one('commisions', 'Commisions', ondelete='cascade', help='Commisions', select=True),
		's_range1':fields.char('Start of Range',size=6),
		'e_range1': fields.char('End of Range',size=6),
		'value1': fields.char('Value',size=3),
	}
	_constraints = [(_check_unique_name, 'Error: Project Value Already Exists', ['s_range1'])]
project_value_line

