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
 _name = "asset"
 _description = "This table is for keeping location data"
 _columns = {
  's_no': fields.integer('S.No', size=100),
  'asset_id': fields.char('Id',size=20),
  'name': fields.char('Asset Type Name', size=100,required=True, select=True),
  'asset_code': fields.char('Asset Code', size=20),
  'asset_line': fields.one2many('asset.line', 'asset_line_id','Asset Lines', select=True, required=True),
 }
asset


class asset_line(osv.osv):

 def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
  
  res = super(asset_line, self).read(cr, uid,ids, fields, context, load)
  seq_number =0 
  for r in res:
   seq_number = seq_number+1
   r['sr_no'] = seq_number
  
  return res
 _name = "asset.line"
 _description = "This table is for keeping location data"
 _columns = {
  'sr_no': fields.integer('S.No', size=100),
  'line_id': fields.char('Id',size=20),
  'brand': fields.char('Brand', size=100,required=True, select=True),
  'model': fields.char('Model', size=20),
  'specs': fields.char('Specs & Desc', size=20),
  'date_issue': fields.date('Issue Date', size=20),
  'date_stopped': fields.date('Stopped Date', size=20),
  'asset_line_id': fields.many2one('asset', 'Asset', ondelete='cascade', help='Test', select=True),
 }
asset_line ()
