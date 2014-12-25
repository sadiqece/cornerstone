from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class asset(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(asset, self).read(cr, uid,ids, fields, context, load)
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
				x.asset_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.asset_code and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.asset_code and self_obj.asset_code.lower() in  lst:
				return False
		return True

	_name = "asset"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100),
		'name': fields.char('Asset Type Name', size=100,required=True, select=True),
		'asset_code': fields.char('Asset Code', size=20),
		'asset_line': fields.one2many('asset.line', 'sr_no','Asset Lines', select=True, required=True),
	}
	_constraints = [(_check_unique_name, 'Error: Asset Name Already Exists', ['name']),(_check_unique_code, 'Error: Asset Code Already Exists', ['asset_code'])]
asset

class master_brand(osv.osv):
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
	_name ='master.brand'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Brand',size=20),
	}
	_constraints = [(_check_unique_name, 'Error: Brand Already Exists', ['name'])]
master_brand()


class asset_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(asset_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res

	def months_between(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
	   
	def onchange_issuedate(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.datetime.now().date()))
			res = {'value':{}}
			if d > 0:
				res['value']['date_issue'] = ''
				#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, Past date not allowed.')}})
				return res
			return dob
			
	def onchange_stopeddate(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.datetime.now().date()))
			res = {'value':{}}
			if d > 0:
				res['value']['date_stopped'] = ''
				#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, Past date not allowed.')}})
				return res
			return dob
			
	def _check_unique_issuedate(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.date_issue for x in self.browse(cr, uid, sr_ids, context=context)
				if x.date_issue and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.date_issue and self_obj.date_issue in  lst:
				return False
		return True
		
	def _check_unique_stopeddate(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.date_stopped for x in self.browse(cr, uid, sr_ids, context=context)
				if x.date_stopped and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.date_stopped and self_obj.date_stopped in  lst:
				return False
		return True

	_name = "asset.line"
	_description = "This table is for keeping location data"
	_columns = {
		'sr_no': fields.integer('S.No', size=100, readonly=1),
		#'line_id': fields.char('Id',size=20),
		'brand':fields.many2one('master.brand', 'Brand', ondelete='cascade', help='Description', select=True,required=True),
		'model': fields.char('Model', size=20),
		'specs': fields.char('Specs & Description', size=20),
		'date_issue': fields.date('Date of First Issue'),
		'date_stopped': fields.date('Date Stopped Issuing'),
		'asset_line_id': fields.many2one('asset', 'Asset', ondelete='cascade', help='Test', select=True),
	}
	_constraints = [(_check_unique_issuedate, 'Error: Date Already Exists', ['date_issue']),(_check_unique_stopeddate, 'Error: Date Already Exists', ['date_stopped'])]
asset_line ()
