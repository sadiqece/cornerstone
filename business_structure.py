from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class business(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(business, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _calculate_total_mod(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = self.browse(cr, uid, ids[0], context=context).people_line or []
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
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
				x.business_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.business_code and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.business_code and self_obj.business_code.lower() in  lst:
				return False
		return True
		
	_name = "business"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100,readonly=1),
		'business_id': fields.char('Id',size=20),
		'name': fields.char('Business Unit Name', size=100,required=True, select=True),
		'business_code': fields.char('Business Code', size=20),
		'bussiness_id':fields.many2one('business', 'Partner', ondelete='cascade', help='Bussiness', select=True),
		'unit_line': fields.one2many('unit.line', 'unit_line_id', 'Unit Lines', select=True, required=True),
		'people_line': fields.one2many('people.line', 'people_line_id', 'People Lines', select=True, required=True),
		'people_count': fields.function(_calculate_total_mod, relation="business",readonly=1,string='People Count',type='integer'),
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
	_constraints = [(_check_unique_name, 'Error: Name already exist', ['name']),(_check_unique_code, 'Error: Code already exist', ['business_code'])]
business


class unit_line(osv.osv):

	def _check_unique_order_priority(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.order_priority.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.order_priority and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.order_priority and self_obj.order_priority.lower() in  lst:
				return False
		return True

	_name = "unit.line"
	_description = "This table is for keeping location data"
	_columns = {
		'u_line_id': fields.char('Id',size=20),
		'order_priority': fields.char('Order Of Priority', size=2,required=True, select=True),
		'unit': fields.char('Unit', size=30),
		'unit_line_id': fields.many2one('business', 'Business', ondelete='cascade', help='Test', select=True),
	}
	_constraints = [(_check_unique_order_priority, 'Error: Order of Priority should be unique', ['order_priority'])]
unit_line

class people_line(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(people_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	def _check_unique_order_priority(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True	
		
	_name = "people.line"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100,readonly=1),
		'p_line_id': fields.char('Id',size=20),
		'name': fields.char('Name', size=20,required=True, select=True),
		'title': fields.char('Title', size=20),
		'people_line_id': fields.many2one('business', 'Business', ondelete='cascade', help='Test', select=True),
	}
	_constraints = [(_check_unique_order_priority, 'Error: Name already exist', ['name'])]
people_line