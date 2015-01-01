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

	_name = "commisions"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100, readonly=1),
		'commision_id': fields.char('Id',size=20),
		'name': fields.char('Commisions Name', size=100,required=True, select=True),
		'commision_code': fields.char('Commisions Code', size=20),
		'pay_value': fields.selection((('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')),'Pay Out Value in $'),
		'program_line': fields.one2many('program.line', 'program_line_id', 'Program Lines', select=True, required=True),
		'bussiness_id':fields.many2one('business', 'Applied To', ondelete='cascade', help='Bussiness', select=True),
		'applied_to': fields.integer('Applied To',size=10),
		'date_added': fields.date('Date Added'),
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
commisions

class program_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(program_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	_name = "program.line"
	_description = "Module Line"
	_columns = {
		's_no': fields.integer('S.No', size=100, readonly=1),
		'program_line_id': fields.many2one('commisions', 'Commisions', ondelete='cascade', help='Commisions', select=True),
		'program_id':fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True, required=True),
		'program_code': fields.related('program_id','program_code',type="char",relation="lis.program",string="Program Code", readonly=1),
		'value': fields.char('Value',size=20),
	}
program_line

class commisions_1(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(commisions_1, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res

	_name = "commisions_1"
	_description = "This table is for keeping location data"
	_columns = {
		'sr_no': fields.integer('S.No', size=100),
		'commision_id': fields.char('Id',size=20),
		'name': fields.char('Commisions Name', size=100,required=True, select=True),
		'commision_code': fields.char('Commisions Code', size=20),
		'pay_value': fields.selection((('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')),'Pay Out Value in %'),
		'project_value_line': fields.one2many('project.value.line', 'project_value_line_id', 'Project Lines', select=True, required=True),
		'bussiness_id': fields.many2one('business', 'Applied To', ondelete='cascade', help='Bussiness', select=True),
		'date_added1': fields.date('Date Added'),
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
commisions_1



class project_value_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(project_value_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res
	_name = "project.value.line"
	_description = "Project Line"
	_columns = {
		'sr_no': fields.integer('S.No', size=100, readonly=1),
		'project_value_line_id': fields.many2one('commisions_1', 'Commisions', ondelete='cascade', help='Commisions', select=True),
		's_range':fields.char('Start of Range',size=20),
		'e_range': fields.char('End of Range',size=20),
		'value': fields.char('Value',size=20),
	}
project_value_line

