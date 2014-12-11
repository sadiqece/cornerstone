import datetime
from dateutil import relativedelta
from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class holidays(osv.osv):
	
	def _populate_year(self, cursor, user_id, context=None):
		return ( 
		   ('choice1', '2010'),
		   ('choice2', '2011'),
		   ('choice3', '2012'),
		   ('choice4', '2013'),
		   ('choice5', '2014'),
		   ('choice6', '2015'),
		   ('choice7', '2016'),
		   ('choice8', '2017'),
		   ('choice9', '2018'),
		   ('choice10', '2019'),
		   ('choice11', '2020'),
		   ('choice12', '2021'),
		   ('choice13', '2022'),
		   ('choice14', '2023'))
		
	def populate_year(self, cursor, user_id, context=None):
		year_dropdown = ''
		for y in range(2010, (datetime.datetime.now().year + 10)):
			year_dropdown = year_dropdown + '(' + y, y + '),'
		return year_dropdown
		
	_name = "holiday"
	_description = "This table is for keeping location data"
	_columns = {
		'holiday_id': fields.char('Id',size=20),
		'year': fields.selection(_populate_year,'Year',select=True, required=True),
		'holiday_line': fields.one2many('holiday.line', 'holiday_line_id', 'Holiday Lines', select=True, required=True),
	}
holidays


class holiday_line(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
  
	  res = super(holiday_line, self).read(cr, uid,ids, fields, context, load)
	  seq_number =0 
	  for r in res:
	   seq_number = seq_number+1
	   r['s_no'] = seq_number
	   
	   return res
	   
	def _check_unique_start_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.date_start.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.date_start and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.date_start and self_obj.date_start.lower() in  lst:
				return False
		return True
		
	def _check_unique_end_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.date_end.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.date_end and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.date_end and self_obj.date_end.lower() in  lst:
				return False
		return True
		
	def months_between(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
	   
	def onchange_date(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.datetime.now().date()))
			res = {'value':{}}
			if d > 0:
				res['value']['date_start'] = ''
				#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, Past date not allowed.')}})
				return res
			return dob
			
	def onchange_dateend(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.datetime.now().date()))
			res = {'value':{}}
			if d < 0:
				res['value']['date_end'] = ''
				#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, Past date not allowed.')}})
				return res
			return dob		
			
	_name = "holiday.line"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.char('S.No',size=20, readonly=1),
		'description': fields.char('Description', size=100,required=True, select=True),
		'date_start': fields.date('Date Start'),
		'date_end': fields.date('Date End'),
		'holiday_line_id': fields.many2one('holiday', 'Holidays', ondelete='cascade', help='Holiday', select=True),
	}
	_constraints = [(_check_unique_start_date, 'Error: Date Already Exists', ['date_start']),(_check_unique_end_date, 'Error: Date Already Exists', ['date_end'])]
holiday_line
