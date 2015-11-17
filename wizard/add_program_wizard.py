from openerp import addons
from datetime import datetime, timedelta, date
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _


import logging
import pytz
import re
import time
from openerp import tools

class wizard_with_step(osv.osv_memory):
	_name = 'wizard.with.step'
	_description = 'Wizard with step'    
	_columns = { 
				'field_id': fields.many2one('learner.info', 'Write-Off account'),
				'name1': fields.char('Name 1'),
				'name2': fields.char('Name 2'),
				'state': fields.selection([('step1', 'step1'),('step2', 'step2')])  
				} 

	def action_next(self, cr, uid, ids, context=None):
		#your treatment to click  button next 
		#...
		# update state to  step2
		self.write(cr, uid, ids, {'state': 'step2',}, context=context)
		#return view
		return {
				'type': 'ir.actions.act_window',
				'res_model': 'your_wizard',
				'view_mode': 'form',
				'view_type': 'form',
				'res_id': this.id,
				'views': [(False, 'form')],
				'target': 'new',
				}

	def action_previous(self, cr, uid, ids, context=None):
		#your treatment to click  button previous 
		#...
		# update state to  step1
		self.write(cr, uid, ids, {'state': 'step1',}, context=context)
		#return view
		return {
				'type': 'ir.actions.act_window',
				'res_model': 'your_wizard',
				'view_mode': 'form',
				'view_type': 'form',
				'res_id': this.id,
				'views': [(False, 'form')],
				'target': 'new',
				}
wizard_with_step()