from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

####################
#PROGRAMS
####################

#Class Program
###############

class program(osv.osv):

#Dropdown to Show no. of module groups

    def onchange_no_of_mod_gp(self, cr, uid, ids, no_of_mod_gp):
        val = {}
        val['no_module_box1'] = False
        val['no_module_box2'] = False
        val['no_module_box3'] = False
        val['no_module_box4'] = False
        val['no_module_box5'] = False
        val['no_module_box6'] = False
        if no_of_mod_gp == '1':
            val['no_module_box1'] = True
        elif no_of_mod_gp == '2':
            val['no_module_box1'] = True
            val['no_module_box2'] = True
        elif no_of_mod_gp == '3':
            val['no_module_box1'] = True
            val['no_module_box2'] = True
            val['no_module_box3'] = True
        elif no_of_mod_gp == '4':
            val['no_module_box1'] = True
            val['no_module_box2'] = True
            val['no_module_box3'] = True
            val['no_module_box4'] = True
        elif no_of_mod_gp == '5':
            val['no_module_box1'] = True
            val['no_module_box2'] = True
            val['no_module_box3'] = True
            val['no_module_box4'] = True
            val['no_module_box5'] = True
        elif no_of_mod_gp == '6':
            val['no_module_box1'] = True
            val['no_module_box2'] = True
            val['no_module_box3'] = True
            val['no_module_box4'] = True
            val['no_module_box5'] = True
            val['no_module_box6'] = True

        return {'value': val} 

#Set Module as

    def onchange_set_module_as_1(self, cr, uid, ids, set_module_as_1):
        val = {}
        val['set_module_block_1'] = False
        val['set_module_select_1'] = False
        if set_module_as_1 == 'Block':
            val['set_module_block_1'] = True
        elif set_module_as_1 == 'Selectable':
            val['set_module_select_1'] = True

        return {'value': val}

    def onchange_set_module_as_2(self, cr, uid, ids, set_module_as_2):
        val = {}
        val['set_module_block_2'] = False
        val['set_module_select_2'] = False
        if set_module_as_2 == 'Block':
            val['set_module_block_2'] = True
        elif set_module_as_2 == 'Selectable':
            val['set_module_select_2'] = True

        return {'value': val}

    def onchange_set_module_as_3(self, cr, uid, ids, set_module_as_3):
        val = {}
        val['set_module_block_3'] = False
        val['set_module_select_3'] = False
        if set_module_as_3 == 'Block':
            val['set_module_block_3'] = True
        elif set_module_as_3 == 'Selectable':
            val['set_module_select_3'] = True

        return {'value': val}

    def onchange_set_module_as_4(self, cr, uid, ids, set_module_as_4):
        val = {}
        val['set_module_block_4'] = False
        val['set_module_select_4'] = False
        if set_module_as_4 == 'Block':
            val['set_module_block_4'] = True
        elif set_module_as_4 == 'Selectable':
            val['set_module_select_4'] = True

        return {'value': val}

    def onchange_set_module_as_5(self, cr, uid, ids, set_module_as_5):
        val = {}
        val['set_module_block_5'] = False
        val['set_module_select_5'] = False
        if set_module_as_5 == 'Block':
            val['set_module_block_5'] = True
        elif set_module_as_5 == 'Selectable':
            val['set_module_select_5'] = True

        return {'value': val}

    def onchange_set_module_as_6(self, cr, uid, ids, set_module_as_6):
        val = {}
        val['set_module_block_6'] = False
        val['set_module_select_6'] = False
        if set_module_as_6 == 'Block':
            val['set_module_block_6'] = True
        elif set_module_as_6 == 'Selectable':
            val['set_module_select_6'] = True

        return {'value': val}

#To Get Requirements

    def _load_prog_mod_line(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line:
               module_ids.append(prog_module_line['module_id'].id)
           if 'module_id_2' in prog_module_line:
               module_ids.append(prog_module_line['module_id_2'].id)
           if 'module_id_3' in prog_module_line:
               module_ids.append(prog_module_line['module_id_3'].id)
           if 'module_id_4' in prog_module_line:
               module_ids.append(prog_module_line['module_id_4'].id)
           if 'module_id_5' in prog_module_line:
               module_ids.append(prog_module_line['module_id_5'].id)
           if 'module_id_6' in prog_module_line:
               module_ids.append(prog_module_line['module_id_6'].id)
       
       value_ids = self.pool.get('req.module').search(cr, uid, [('mod_id', 'in', module_ids)])
       return dict([(id, value_ids) for id in ids])

    def _load_prog_mod_show_do_line(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_ids = prog_mod_obj.search(cr, uid, [('prog_mod_id', '=', ids[0])])
       module_ids =[]
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           module_ids.append(prog_module_line['module_id'].id)
       
       value_ids = self.pool.get('req.module').search(cr, uid, [('mod_id', 'in', module_ids),('verification', '=', True)])
       return dict([(id, value_ids) for id in ids])

#To Get Show Do

    def _load_prog_show_do_line(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line:
               module_ids.append(prog_module_line['module_id'].id)
           if 'module_id_2' in prog_module_line:
               module_ids.append(prog_module_line['module_id_2'].id)
           if 'module_id_3' in prog_module_line:
               module_ids.append(prog_module_line['module_id_3'].id)
           if 'module_id_4' in prog_module_line:
               module_ids.append(prog_module_line['module_id_4'].id)
           if 'module_id_5' in prog_module_line:
               module_ids.append(prog_module_line['module_id_5'].id)
           if 'module_id_6' in prog_module_line:
               module_ids.append(prog_module_line['module_id_6'].id)
       
       value_ids = self.pool.get('show.do.module').search(cr, uid, [('mod_id', 'in', module_ids)])
       return dict([(id, value_ids) for id in ids])

#Load data For Multiple Tabs

    def _load_module_info(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line:
               module_ids.append(prog_module_line['module_id'].id)
           if 'module_id_2' in prog_module_line:
               module_ids.append(prog_module_line['module_id_2'].id)
           if 'module_id_3' in prog_module_line:
               module_ids.append(prog_module_line['module_id_3'].id)
           if 'module_id_4' in prog_module_line:
               module_ids.append(prog_module_line['module_id_4'].id)
           if 'module_id_5' in prog_module_line:
               module_ids.append(prog_module_line['module_id_5'].id)
           if 'module_id_6' in prog_module_line:
               module_ids.append(prog_module_line['module_id_6'].id)  
       value_ids = self.pool.get('cs.module').search(cr, uid, [('id', 'in', module_ids)])
       return dict([(id, value_ids ) for id in ids])
       
#Max Fee

    def _calculate_total_fee_max(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_obj2 = self.pool.get('lis.program')
       lis_program = prog_mod_obj2.browse(cr, uid, ids[0],context=context)
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       res = {}
       max_fee = 0.00
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line and prog_module_line['module_id'] != False:
               module_ids.append(prog_module_line['module_id'].id)
           #2
           if 'module_id_2' in prog_module_line and prog_module_line['module_id_2'] != False:
               module_ids.append(prog_module_line['module_id_2'].id)
           #3
           if 'module_id_3' in prog_module_line and prog_module_line['module_id_3'] != False:
               module_ids.append(prog_module_line['module_id_3'].id)
           #4
           if 'module_id_4' in prog_module_line and prog_module_line['module_id_4'] != False:
               module_ids.append(prog_module_line['module_id_4'].id)
           #5
           if 'module_id_5' in prog_module_line and prog_module_line['module_id_5'] != False:
               module_ids.append(prog_module_line['module_id_5'].id)
           #6
           if 'module_id_6' in prog_module_line and prog_module_line['module_id_6'] != False:
               module_ids.append(prog_module_line['module_id_6'].id)
       mod_obj = self.pool.get('cs.module').search(cr, uid, [('id', 'in', module_ids)])
       for value_ids in self.pool.get('cs.module').browse(cr, uid, mod_obj):
           max_fee += value_ids['module_fee']
       res[ids[0]] = max_fee
       return res

#Min Fee
   
    def _calculate_total_fee_min(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_obj2 = self.pool.get('lis.program')
       lis_program = prog_mod_obj2.browse(cr, uid, ids[0],context=context)
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       res = {}
       min_fee = 0.00
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line and prog_module_line['module_id'] != False and lis_program['set_group_as_sel_1'] == False:
               module_ids.append(prog_module_line['module_id'].id)
           #2
           if 'module_id_2' in prog_module_line and prog_module_line['module_id_2'] != False and  lis_program['set_group_as_sel_2'] == False:
               module_ids.append(prog_module_line['module_id_2'].id)
           #3
           if 'module_id_3' in prog_module_line and prog_module_line['module_id_3'] != False and lis_program['set_group_as_sel_3'] == False:
               module_ids.append(prog_module_line['module_id_3'].id)
           #4
           if 'module_id_4' in prog_module_line and prog_module_line['module_id_4'] != False and lis_program['set_group_as_sel_4'] == False:
               module_ids.append(prog_module_line['module_id_4'].id)
           #5
           if 'module_id_5' in prog_module_line and prog_module_line['module_id_5'] != False and lis_program['set_group_as_sel_5'] == False:
               module_ids.append(prog_module_line['module_id_5'].id)
           #6
           if 'module_id_6' in prog_module_line and prog_module_line['module_id_6'] != False and lis_program['set_group_as_sel_6'] == False:
               module_ids.append(prog_module_line['module_id_6'].id)
       mod_obj = self.pool.get('cs.module').search(cr, uid, [('id', 'in', module_ids)])
       for value_ids in self.pool.get('cs.module').browse(cr, uid, mod_obj):
           min_fee += value_ids['module_fee']
       res[ids[0]] = min_fee
       return res

#Min Modules

    def _calculate_total_mod_min(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_obj2 = self.pool.get('lis.program')
       lis_program = prog_mod_obj2.browse(cr, uid, ids[0],context=context)
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       res = {}
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line and prog_module_line['module_id'] != False and lis_program['set_group_as_sel_1'] == False:
               module_ids.append(prog_module_line['module_id'].id)
           #2
           if 'module_id_2' in prog_module_line and prog_module_line['module_id_2'] != False and  lis_program['set_group_as_sel_2'] == False:
               module_ids.append(prog_module_line['module_id_2'].id)
           #3
           if 'module_id_3' in prog_module_line and prog_module_line['module_id_3'] != False and lis_program['set_group_as_sel_3'] == False:
               module_ids.append(prog_module_line['module_id_3'].id)
           #4
           if 'module_id_4' in prog_module_line and prog_module_line['module_id_4'] != False and lis_program['set_group_as_sel_4'] == False:
               module_ids.append(prog_module_line['module_id_4'].id)
           #5
           if 'module_id_5' in prog_module_line and prog_module_line['module_id_5'] != False and lis_program['set_group_as_sel_5'] == False:
               module_ids.append(prog_module_line['module_id_5'].id)
           #6
           if 'module_id_6' in prog_module_line and prog_module_line['module_id_6'] != False and lis_program['set_group_as_sel_6'] == False:
               module_ids.append(prog_module_line['module_id_6'].id)

       value_ids = self.pool.get('cs.module').search(cr, uid, [('id', 'in', module_ids)])
       min_mod = len(value_ids)
       res[ids[0]] = min_mod
       return res

#Max Modules 
 
    def _calculate_total_mod_max(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_obj2 = self.pool.get('lis.program')
       lis_program = prog_mod_obj2.browse(cr, uid, ids[0],context=context)
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       res = {}
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line and prog_module_line['module_id'] != False:
               module_ids.append(prog_module_line['module_id'].id)
           #2
           if 'module_id_2' in prog_module_line and prog_module_line['module_id_2'] != False:
               module_ids.append(prog_module_line['module_id_2'].id)
           #3
           if 'module_id_3' in prog_module_line and prog_module_line['module_id_3'] != False:
               module_ids.append(prog_module_line['module_id_3'].id)
           #4
           if 'module_id_4' in prog_module_line and prog_module_line['module_id_4'] != False:
               module_ids.append(prog_module_line['module_id_4'].id)
           #5
           if 'module_id_5' in prog_module_line and prog_module_line['module_id_5'] != False:
               module_ids.append(prog_module_line['module_id_5'].id)
           #6
           if 'module_id_6' in prog_module_line and prog_module_line['module_id_6'] != False:
               module_ids.append(prog_module_line['module_id_6'].id)

       value_ids = self.pool.get('cs.module').search(cr, uid, [('id', 'in', module_ids)])
       max_mod = len(value_ids)
       res[ids[0]] = max_mod
       return res

#Max Duration
 
    def _calculate_total_duration_max(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_obj2 = self.pool.get('lis.program')
       lis_program = prog_mod_obj2.browse(cr, uid, ids[0],context=context)
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       res = {}
       max_dur = 0.00
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line and prog_module_line['module_id'] != False:
               module_ids.append(prog_module_line['module_id'].id)
           #2
           if 'module_id_2' in prog_module_line and prog_module_line['module_id_2'] != False:
               module_ids.append(prog_module_line['module_id_2'].id)
           #3
           if 'module_id_3' in prog_module_line and prog_module_line['module_id_3'] != False:
               module_ids.append(prog_module_line['module_id_3'].id)
           #4
           if 'module_id_4' in prog_module_line and prog_module_line['module_id_4'] != False:
               module_ids.append(prog_module_line['module_id_4'].id)
           #5
           if 'module_id_5' in prog_module_line and prog_module_line['module_id_5'] != False:
               module_ids.append(prog_module_line['module_id_5'].id)
           #6
           if 'module_id_6' in prog_module_line and prog_module_line['module_id_6'] != False:
               module_ids.append(prog_module_line['module_id_6'].id)
       mod_obj = self.pool.get('cs.module').search(cr, uid, [('id', 'in', module_ids)])
       for value_ids in self.pool.get('cs.module').browse(cr, uid, mod_obj):
           max_dur += value_ids['module_duration']
       res[ids[0]] = max_dur
       return res

#Min Duration

    def _calculate_total_duration_min(self, cr, uid, ids, field_names, args,  context=None):
       prog_mod_obj = self.pool.get('program.module.line')
       prog_mod_obj2 = self.pool.get('lis.program')
       lis_program = prog_mod_obj2.browse(cr, uid, ids[0],context=context)
       prog_mod_ids = prog_mod_obj.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', ids[0]),('prog_mod_id_2', '=', ids[0]),('prog_mod_id_3', '=', ids[0]),('prog_mod_id_4', '=', ids[0]),('prog_mod_id_5', '=', ids[0]),('prog_mod_id_6', '=', ids[0])])
       module_ids =[]
       res = {}
       min_dur = 0.00
       for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
           if 'module_id' in prog_module_line and prog_module_line['module_id'] != False and lis_program['set_group_as_sel_1'] == False:
               module_ids.append(prog_module_line['module_id'].id)
           #2
           if 'module_id_2' in prog_module_line and prog_module_line['module_id_2'] != False and  lis_program['set_group_as_sel_2'] == False:
               module_ids.append(prog_module_line['module_id_2'].id)
           #3
           if 'module_id_3' in prog_module_line and prog_module_line['module_id_3'] != False and lis_program['set_group_as_sel_3'] == False:
               module_ids.append(prog_module_line['module_id_3'].id)
           #4
           if 'module_id_4' in prog_module_line and prog_module_line['module_id_4'] != False and lis_program['set_group_as_sel_4'] == False:
               module_ids.append(prog_module_line['module_id_4'].id)
           #5
           if 'module_id_5' in prog_module_line and prog_module_line['module_id_5'] != False and lis_program['set_group_as_sel_5'] == False:
               module_ids.append(prog_module_line['module_id_5'].id)
           #6
           if 'module_id_6' in prog_module_line and prog_module_line['module_id_6'] != False and lis_program['set_group_as_sel_6'] == False:
               module_ids.append(prog_module_line['module_id_6'].id)
       mod_obj = self.pool.get('cs.module').search(cr, uid, [('id', 'in', module_ids)])
       for value_ids in self.pool.get('cs.module').browse(cr, uid, mod_obj):
           min_dur += value_ids['module_duration']
       res[ids[0]] = min_dur
       return res

#Total Credit
   
    def _calculate_total_credit(self, cr, uid, ids, field_names, args,  context=None):
       res = {}
       for line in self.browse(cr, uid, ids, context=context):
          total_credit =0
          prog_mod_obj = self.pool.get('program.module.line')
          prog_mod_ids = prog_mod_obj.search(cr, uid, [('prog_mod_id', '=', line.id)])
          if len(prog_mod_ids) > 0:
            module_ids =[]
            for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
              if type(prog_module_line['module_id'].id) == int:
                 module_ids.append(prog_module_line['module_id'].id)
                 
            if len(module_ids) > 0:
              for module_obj in self.pool.get('cs.module').browse(cr, uid, module_ids):
                  total_credit += module_obj['module_credit_value']
          res[line.id] = total_credit
       return res

#Program Status

    def _prog_status_display(self, cr, uid, ids, field_names, args,  context=None):
       if not ids: return {}
       res = {}

       for line in self.browse(cr, uid, ids, context=context):
          
          res[line.id] = line['program_status']
       return res

    def _prog_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
       if not ids: return {}
       res = {}

       for line in self.browse(cr, uid, ids, context=context):
          res[line.id] = line['program_status']
       return res
	   
#Unique Module Group Name
    def _check_unique_group(self, cr, uid, ids, context=None):
        new_class = self.browse(cr, uid, ids, context=context)
        _logger.info('Mod G1 = %s', new_class[0].mod_gp_name_1)
        _logger.info('Mod G2 = %s', new_class[0].mod_gp_name_2)
        _logger.info('Mod G3 = %s', new_class[0].mod_gp_name_3)
        _logger.info('Mod G4 = %s', new_class[0].mod_gp_name_4)
        _logger.info('Mod G5 = %s', new_class[0].mod_gp_name_5)
        _logger.info('Mod G6 = %s', new_class[0].mod_gp_name_6)
        for x in range (1,7):
            _logger.info('Mod ALL = %s', new_class[0]['mod_gp_name_'+str(x)])
            if new_class[0].mod_gp_name_1 != False and x != 1 and new_class[0].mod_gp_name_1 == new_class[0]['mod_gp_name_'+str(x)]:                
                return False
            elif new_class[0].mod_gp_name_2 != False and x != 2 and new_class[0].mod_gp_name_2 == new_class[0]['mod_gp_name_'+str(x)]: 
                return False
            elif new_class[0].mod_gp_name_3 != False and x != 3 and new_class[0].mod_gp_name_3 == new_class[0]['mod_gp_name_'+str(x)]: 
                return False
            elif new_class[0].mod_gp_name_4 != False and x != 4 and new_class[0].mod_gp_name_4 == new_class[0]['mod_gp_name_'+str(x)]: 
                return False
            elif new_class[0].mod_gp_name_5 != False and x != 5 and new_class[0].mod_gp_name_5 == new_class[0]['mod_gp_name_'+str(x)]: 
                return False
            elif new_class[0].mod_gp_name_6 != False and x != 6 and new_class[0].mod_gp_name_6 == new_class[0]['mod_gp_name_'+str(x)]: 
                return False
        return True

#History
    def create(self,cr, uid, values, context=None):
       sub_lines = []
       current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
       sub_lines.append( (0,0, {'date_created':fields.date.today(),'created_by':current_user['name'],
            'last_update':'-','last_update_by':'-','date_status_change':fields.date.today(),'status_change_by':current_user['name']}) )
       values.update({'program_history_line': sub_lines})
       module_id = super(program, self).create(cr, uid, values, context=context)
       return module_id  
    
    def write(self,cr, uid, ids, values, context=None):
       sub_lines = []
       
       current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
       for line in self.browse(cr, uid, ids, context=context):
         history_line_id = self.browse(cr, uid, ids[0], context=context).program_history_line or []

       num_of_his = len(history_line_id)-1 
       staus_changed_by =   history_line_id[num_of_his]['status_change_by']
       staus_changed_date =   history_line_id[num_of_his]['date_status_change']
 
       if 'program_status' in values:
          staus_changed_date = fields.date.today()
          staus_changed_by  = current_user['name']
          values['date3'] = fields.date.today()
          values['date4'] = fields.date.today()

       changes = values.keys()
       program_list ={'name': 'Program Name','program_code': 'Program Code','program_level':'Level','program_category':'Category',
             'program_pathway': 'Pathway','program_status': 'Status','program_center': 'Center','program_audience': 'Target Audience',
             'program_description': 'Description','program_synopsis':'Synopsis','program_outline':'Outline',
             'program_cert_achevied':'Certifications Acheived','program_mod_line': 'Module Lines','program_show_do_line': 'Program Show Do',
             'subsidy_line': 'Program Subsidy Items','program_alert_line': 'Alerts for Program'}
       arr={}
       for i in range(len(changes)):
          if changes[i] in program_list:
             arr[i] = program_list[changes[i]]
  
       sub_lines.append( (0,0, {'date_created':history_line_id[0]['date_created'],'created_by':history_line_id[0]['created_by'],
            'last_update':fields.date.today(),'last_update_by':current_user['name'],'date_status_change':staus_changed_date,'status_change_by':staus_changed_by,'changes':arr.values()}) )
       values.update({'program_history_line': sub_lines})
       module_id = super(program, self).write(cr, uid, ids,values, context=context)
       return module_id
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
       
       res = super(program, self).read(cr, uid,ids, fields, context, load)
       seq_number =0 
       for r in res:
       	seq_number = seq_number+1
       	r['s_no'] = seq_number
       
       return res

#Program Desc
    def on_change_program_desc(self, cr, uid, ids, program_description):
       return {'value': {'program_synopsis': program_description}}

#Program Synopsis
    def on_change_program_synopsis(self, cr, uid, ids, program_synopsis):
       return {'value': {'program_description': program_synopsis}} 

#Validate Program Name
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

#Validate Program Code
    def _check_unique_code(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        lst = [
                x.program_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
                if x.program_code and x.id not in ids
              ]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.program_code and self_obj.program_code.lower() in  lst:
               return False
        return True

#Validate Min Max values for Module Blocks
#1
    def _check_min_max_1(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.min_no_modules_1 < 0 or self_obj.max_no_modules_1 < self_obj.min_no_modules_1:
                return False
        return True
#2
    def _check_min_max_2(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.min_no_modules_2 < 0 or self_obj.max_no_modules_2 < self_obj.min_no_modules_2:
                return False
        return True
#3
    def _check_min_max_3(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.min_no_modules_3 < 0 or self_obj.max_no_modules_3 < self_obj.min_no_modules_3:
                return False
        return True
#4
    def _check_min_max_4(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.min_no_modules_4 < 0 or self_obj.max_no_modules_4 < self_obj.min_no_modules_4:
                return False
        return True
#5
    def _check_min_max_5(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.min_no_modules_5 < 0 or self_obj.max_no_modules_5 < self_obj.min_no_modules_5:
                return False
        return True
#6
    def _check_min_max_6(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.min_no_modules_6 < 0 or self_obj.max_no_modules_6 < self_obj.min_no_modules_6:
                return False
        return True

#Table For Class Program 'lis_program'
    _name = "lis.program"
    _description = "This table is for keeping lab data of cord blood"
    _columns = {
        'program_id': fields.char('Id',size=20),
        's_no': fields.char('S.No',size=20),
        'name': fields.char('Program Name', size=100,required=True, select=True),
        'program_code': fields.char('Program Code', size=20),
		'program_level': fields.selection((('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')),'Level'),
	    'program_category':fields.selection((('WPL','WPL'),('WPN','WPN'),('WPS','WPS'),('EDGE','EDGE'),('LPM','LPM'),('SV','SV'),('Non WSQ','Non WSQ')),'Category'),
	    'program_pathway': fields.selection((('Generic','Generic'),('Sectorial','Sectorial'),('Contextualized','Contextualized')),'Pathway'),
		#Max Min
		'max_program_duration': fields.function(_calculate_total_duration_max, relation="lis.program",readonly=1,string='Max Program Duration',type='float', required=True),
		'min_program_duration': fields.function(_calculate_total_duration_min, relation="lis.program",readonly=1,string='Min Program Duration',type='float', required=True),
		'max_program_mod': fields.function(_calculate_total_mod_max, relation="lis.program",readonly=1,string='Max Modules',type='integer'),
		'min_program_mod': fields.function(_calculate_total_mod_min, relation="lis.program",readonly=1,string='Min Modules',type='integer'),
		'max_program_fee': fields.function(_calculate_total_fee_max, relation="lis.program",readonly=1,string='Max Program Fee',type='float'),
		'min_program_fee': fields.function(_calculate_total_fee_min, relation="lis.program",readonly=1,string='Min Program Fee',type='float'),
		'program_tot_credit': fields.function(_calculate_total_credit, relation="lis.program",readonly=1,string='Total Credit',type='integer'),
		'program_status': fields.selection((('Incomplete','Incomplete'),('Active','Active'),('InActive','InActive'),('Completed','Completed')),'Status',required=True, select=True),
		'program_center': fields.selection((('Hougang','Hougang'),('Jurong','Jurong'),('Tampines','Tampines'),('Woodlands','Woodlands')),'Select Center'),
		'select_module': fields.selection((('Module 1','Module 1'),('Module 2','Module 2'),('Module 3','Module 3'),('Module 4','Module 4')),'Select Module'),
		'program_audience': fields.selection((('LWW','LWW'),('LWW','LWW')),'Target Audience'),
		'program_description': fields.text('Description', size=500),
		'program_synopsis':fields.text('Synopsis'),
		'program_outline':fields.text('Outline'),
		'program_cert_achevied': fields.char('Certifications Acheived', size=100),
		#Table in Module Group
		'program_mod_line': fields.one2many('program.module.line', 'prog_mod_id', 'Order Lines', select=True, required=True),
		'program_mod_line_2': fields.one2many('program.module.line', 'prog_mod_id_2', 'Order Lines', select=True, required=True),
		'program_mod_line_3': fields.one2many('program.module.line', 'prog_mod_id_3', 'Order Lines', select=True, required=True),
		'program_mod_line_4': fields.one2many('program.module.line', 'prog_mod_id_4', 'Order Lines', select=True, required=True),
		'program_mod_line_5': fields.one2many('program.module.line', 'prog_mod_id_5', 'Order Lines', select=True, required=True),
		'program_mod_line_6': fields.one2many('program.module.line', 'prog_mod_id_6', 'Order Lines', select=True, required=True),
		'program_module_desc_line': fields.function(_load_module_info, relation="cs.module",readonly=1,string='Module',type='one2many'),
		'program_mod_req_line': fields.function(_load_prog_mod_line, relation="req.module",readonly=1,type='one2many', string='Module'),
		'program_modality_line': fields.function(_load_module_info, relation="cs.module",readonly=1,type='one2many', string='Module'),
		'program_pf_line': fields.function(_load_module_info, relation="cs.module",readonly=1,type='one2many',string='Module'),
		'program_show_do_line': fields.one2many('program.show.do.module','program_id','Show Do'),
		'program_module_show_do_line':  fields.function(_load_prog_mod_show_do_line, relation="req.module",readonly=1,type='one2many', string='Module'),
		'program_test_line': fields.function(_load_module_info, relation="cs.module",readonly=1,type='one2many', string='Module'),
		'subsidy_line': fields.one2many('subsidy.module','program_id','Subsidy Items'),
		'program_cost_line': fields.function(_load_module_info, relation="cs.module",readonly=1,type='one2many', string='Module'),
		'program_alert_line_2': fields.function(_load_module_info, relation="cs.module",readonly=1,type='one2many', string='Module'),
		'program_duration_line': fields.function(_load_module_info, relation="cs.module",readonly=1,type='one2many',string='Module'),
		'program_alert_line': fields.one2many('program.alert.module','program_id','Alerts for Program'),
		'program_module_alerts_line': fields.function(_load_module_info, relation="cs.module", readonly=1, string='Module', type='one2many'),
		'program_history_line': fields.one2many('program.history.module','history_id','History'),
		'prog_status_display': fields.function(_prog_status_display, readonly=1, type='char'),
		'prog_status_display_1': fields.function(_prog_status_display_1, readonly=1, type='char'),
		'date3': fields.date('Date Created', readonly='True'),
		'date4': fields.date('Date Created', readonly='True'),
		'prog_req_line': fields.one2many('program.req.module','req_id','Requirments'),
		#For Multiple Boxes in Module Tab
		'no_of_mod_gp': fields.selection((('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')),'Number of Module Groups'),
		'no_module_box1': fields.boolean('1'),
		'no_module_box2': fields.boolean('2'),
		'no_module_box3': fields.boolean('3'),
		'no_module_box4': fields.boolean('4'),
		'no_module_box5': fields.boolean('5'),
		'no_module_box6': fields.boolean('6'),
		#1
		'mod_gp_name_1': fields.char('Module Group Name'),
		'set_group_as_sel_1': fields.boolean('Set Group As Selectable'),
		'set_module_as_1': fields.selection((('Block','Block'),('Selectable','Selectable')),'Set Module As'),
		'set_module_block_1': fields.boolean('Block'),
		'set_module_select_1': fields.boolean('Selectable'),
		'allow_as_block_1': fields.boolean('Allow scheduling as a block'),
		'min_no_modules_1': fields.integer('Minimum Modules', size=3, select=True),
		'max_no_modules_1': fields.integer('Maximum Modules', size=3, select=True),
		#2
		'mod_gp_name_2': fields.char('Module Group Name'),
		'set_group_as_sel_2': fields.boolean('Set Group As Selectable'),
		'set_module_as_2': fields.selection((('Block','Block'),('Selectable','Selectable')),'Set Module As'),
		'set_module_block_2': fields.boolean('Block'),
		'set_module_select_2': fields.boolean('Selectable'),
		'allow_as_block_2': fields.boolean('Allow scheduling as a block'),
		'min_no_modules_2': fields.integer('Minimum Modules', size=3, select=True),
		'max_no_modules_2': fields.integer('Maximum Modules', size=3, select=True),
		#3
		'mod_gp_name_3': fields.char('Module Group Name'),
		'set_group_as_sel_3': fields.boolean('Set Group As Selectable'),
		'set_module_as_3': fields.selection((('Block','Block'),('Selectable','Selectable')),'Set Module As'),
		'set_module_block_3': fields.boolean('Block'),
		'set_module_select_3': fields.boolean('Selectable'),
		'allow_as_block_3': fields.boolean('Allow scheduling as a block'),
		'min_no_modules_3': fields.integer('Minimum Modules', size=3, select=True),
		'max_no_modules_3': fields.integer('Maximum Modules', size=3, select=True),
		#4
		'mod_gp_name_4': fields.char('Module Group Name'),
		'set_group_as_sel_4': fields.boolean('Set Group As Selectable'),
		'set_module_as_4': fields.selection((('Block','Block'),('Selectable','Selectable')),'Set Module As'),
		'set_module_block_4': fields.boolean('Block'),
		'set_module_select_4': fields.boolean('Selectable'),
		'allow_as_block_4': fields.boolean('Allow scheduling as a block'),
		'min_no_modules_4': fields.integer('Minimum Modules', size=3, select=True),
		'max_no_modules_4': fields.integer('Maximum Modules', size=3, select=True),
		#5
		'mod_gp_name_5': fields.char('Module Group Name'),
		'set_group_as_sel_5': fields.boolean('Set Group As Selectable'),
		'set_module_as_5': fields.selection((('Block','Block'),('Selectable','Selectable')),'Set Module As'),
		'set_module_block_5': fields.boolean('Block'),
		'set_module_select_5': fields.boolean('Selectable'),
		'allow_as_block_5': fields.boolean('Allow scheduling as a block'),
		'min_no_modules_5': fields.integer('Minimum Modules', size=3, select=True),
		'max_no_modules_5': fields.integer('Maximum Modules', size=3, select=True),
		#6
		'mod_gp_name_6': fields.char('Module Group Name'),
		'set_group_as_sel_6': fields.boolean('Set Group As Selectable'),
		'set_module_as_6': fields.selection((('Block','Block'),('Selectable','Selectable')),'Set Module As'),
		'set_module_block_6': fields.boolean('Block'),
		'set_module_select_6': fields.boolean('Selectable'),
		'allow_as_block_6': fields.boolean('Allow scheduling as a block'),
		'min_no_modules_6': fields.integer('Minimum Modules', size=3, select=True),
		'max_no_modules_6': fields.integer('Maximum Modules', size=3, select=True),
    }
	
    _defaults = { 
	   'date3': fields.date.context_today,
	   'date4': fields.date.context_today,
	   'set_group_as_sel_1': True,
	   'set_group_as_sel_2': True,
	   'set_group_as_sel_3': True,
	   'set_group_as_sel_4': True,
	   'set_group_as_sel_5': True,
	   'set_group_as_sel_6': True,
    }
    _constraints = [(_check_unique_name, 'Error: Program Name Already Exists', ['Program Name']),(_check_unique_code, 'Error: Program Code Already Exists', ['Program Code']),(_check_unique_group, 'Error: Module Group Names Cannot Be Same', ['Module Group Name']),(_check_min_max_1, 'Error: Invalid Min/Max Values', ['Module Group 1']),(_check_min_max_2, 'Error: Invalid Min/Max Values', ['Module Group 2']),(_check_min_max_3, 'Error: Invalid Min/Max Values', ['Module Group 3']),(_check_min_max_4, 'Error: Invalid Min/Max Values', ['Module Group 4']),(_check_min_max_5, 'Error: Invalid Min/Max Values', ['Module Group 5']),(_check_min_max_6, 'Error: Invalid Min/Max Values', ['Module Group 6'])]
program()


#Class program_mod_line
###############

globvar = 0
class program_mod_line(osv.osv):

#Validate Unique Modules
	def _check_unique_module(self, cr, uid, ids, context=None):
		new_class = self.browse(cr, uid, ids, context=context)
		module_id = -1
		program_id = -1
		for x in range (1,7) :
			if x == 1 :
				name = 'module_id'
				name1 = 'prog_mod_id'
			else :
				name = 'module_id_'+str(x)
				name1 = 'prog_mod_id_'+str(x)
				
			if module_id == -1 and new_class[0][name]['id'] != False and new_class[0][name]['id'] != None :
				module_id = new_class[0][name]['id']
			
			if program_id == -1 and new_class[0][name1]['id'] != False  and new_class[0][name1]['id'] != None:
				program_id = new_class[0][name1]['id']
				
				
		sr_ids = self.search(cr, uid, ['|','|','|','|','|',('prog_mod_id', '=', program_id),('prog_mod_id_2', '=', program_id),('prog_mod_id_3', '=', program_id),('prog_mod_id_4', '=', program_id),('prog_mod_id_5', '=', program_id),('prog_mod_id_6', '=', program_id)])
		
		for x in self.browse(cr, uid, sr_ids, context=context) : 
			for r in range (1,7) :
				if r == 1 :
					name = 'module_id'
				else :
					name = 'module_id_'+str(r)
				
				if new_class[0].id != x.id and x[name]['id'] != None and x[name]['id'] == module_id:
					return False
					
		return True
		
# Table for Module Group
	_name = "program.module.line"
	_description = "Module Line"
	_columns = {
		'prog_mod_id': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, store=True),
		'module_code': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'no_of_hrs': fields.related('module_id','module_duration',type="float",relation="cs.module",string="Module Duration", readonly=1, required=True),  
		#2
		'prog_mod_id_2': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id_2':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, store=True),
		'module_code_2': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'no_of_hrs_2': fields.related('module_id','module_duration',type="float",relation="cs.module",string="Module Duration", readonly=1, required=True), 
		#3
		'prog_mod_id_3': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id_3':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, store=True),
		'module_code_3': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'no_of_hrs_3': fields.related('module_id','module_duration',type="float",relation="cs.module",string="Module Duration", readonly=1, required=True), 
		#4
		'prog_mod_id_4': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id_4':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, store=True),
		'module_code_4': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'no_of_hrs_4': fields.related('module_id','module_duration',type="float",relation="cs.module",string="Module Duration", readonly=1, required=True), 
		#5
		'prog_mod_id_5': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id_5':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, store=True),
		'module_code_5': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'no_of_hrs_5': fields.related('module_id','module_duration',type="float",relation="cs.module",string="Module Duration", readonly=1, required=True), 
		#6
		'prog_mod_id_6': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id_6':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, store=True),
		'module_code_6': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),
		'no_of_hrs_6': fields.related('module_id','module_duration',type="float",relation="cs.module",string="Module Duration", readonly=1, required=True), 
    }

	_constraints = [(_check_unique_module, 'Error: Module Already Exists', ['Module'])]

program_mod_line()

#Class Program Requirements
###############

class program_requirments(osv.osv):
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('req.module')
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

	def on_change_program_master_req(self, cr, uid, ids, module_req):
		if not module_req: return {}
		master_req_obj = self.pool.get('master.req').browse(cr, uid, module_req)
		return {'value': {'description': master_req_obj.description,'musthave':master_req_obj.musthave,'verification':master_req_obj.verification}}
		
	def create(self,cr, uid, values, context=None):
		module_id = super(program_requirments, self).create(cr, uid, values, context=context)
		line_id=[]
		line_id.append(values['program_master_req'])
		self.pool.get('master.req').write(cr, uid, line_id,{'description':values['description'],
		'musthave':values['musthave'],'verification':values['verification']}, context=context)
		return module_id

#Validate Unique Label
	def _check_unique_label(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.req_id == self_obj.req_id and x.program_master_req == self_obj.program_master_req:
						return False
		return True
		
# Table for Program req.module

	_name ='program.req.module'
	_description ="Requirement Tab"
	_columns = {
	'req_id':fields.integer('S.No',size=20),
	'program_master_req':fields.many2one('master.req', 'Label', ondelete='cascade', help='Requirements', select=True,required=True),
	'description':fields.char('Description',size=20),
	'musthave':fields.boolean('Must Have'),
	'verification':fields.boolean('Verification'),
	'module_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module'),
	}
	
	_constraints = [(_check_unique_label, 'Error: Label Already Exists', ['Label'])]
program_requirments()

#Class Program Master Requirements
###############

class program_master_req(osv.osv):
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
	_name ='master.req'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Label',size=20,required=True),
	'description':fields.char('Description',size=100),
	'musthave':fields.boolean('Must Have'),
	'verification':fields.boolean('Verification'),
	}
	_constraints = [(_check_unique_name, 'Error: Requirement Label Already Exists', ['Requirement'])]
program_master_req()

#Class Program Show Do
###############
class program_show_do(osv.osv):

	def on_change_master_show_do(self, cr, uid, ids, master_show_do):
		master_show_do_obj = self.pool.get('master.show.do').browse(cr, uid, master_show_do)
		return {'value': {'supp_doc_req': master_show_do_obj.supp_doc_req}}
	def _check_unique_prog_show_do(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.program_id == self_obj.program_id and x.master_show_do == self_obj.master_show_do:
						return False
		return True
	_name ='program.show.do.module'
	_description ="Show & Do Tab"
	_columns = {
	'show_do_id':fields.integer('S.No',size=20),
	'master_show_do':fields.many2one('master.show.do', 'Item', ondelete='cascade', help='Show & Do', select=True, required=True),
	'supp_doc_req':fields.boolean('Supporting Document Required'),
	'program_id': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Module'),
	}
	_constraints = [(_check_unique_prog_show_do, 'Error: Item Already Exists', ['Show and Do'])]
program_show_do()

#Class Program Master Show Do
###############
class master_show_do(osv.osv):
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
	_name ='master.show.do'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Item',size=20),
	'supp_doc_req':fields.boolean('Supporting Document Required')
	}
	_constraints = [(_check_unique_name, 'Error: Item Already Exists', ['name'])]
master_show_do()

#Class Program Master Subsidy
###############

class master_subsidy(osv.osv):
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
	_name ='master.subsidy'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Description',size=20, required=True),
	'per_fee_mod':fields.integer('% Of Module Fee',size=3),
	'ver_req':fields.boolean('Verification Required')
	}
	_constraints = [(_check_unique_name, 'Error: Description Already Exists', ['name'])]
master_subsidy()

#Class Program Subsidy
###############
class program_subsidy(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(program_subsidy, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	def on_change_master_subsidy(self, cr, uid, ids, master_show_do):
		master_show_do_obj = self.pool.get('master.subsidy').browse(cr, uid, master_show_do)
		return {'value': {'per_fee_mod': master_show_do_obj.per_fee_mod,'ver_req': master_show_do_obj.ver_req}}
	def _check_unique_prog_subs(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.program_id == self_obj.program_id and x.master_subsidy == self_obj.master_subsidy:
						return False
		return True
	def on_change_per_fee_mod(self, cr, uid, ids, per_fee_mod):
		if per_fee_mod < 0:
			raise osv.except_osv(_('Error!'),_("Module Fee - Cannot be negative value"))
		return per_fee_mod
		
#Validate Subsidy Negative
	def validate_neg_fee_mod(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.per_fee_mod < 0:
				return False
		return True
	_name ='subsidy.module'
	_description ="People and Facilites Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'cost_id':fields.integer('Id',size=20),
	'master_subsidy':fields.many2one('master.subsidy', 'Description', ondelete='cascade', help='Show & Do', select=True, required=True),
	'per_fee_mod':fields.integer('% Of Module Fee',size=3),
	'ver_req':fields.boolean('Verification Required'),
	'program_id': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Module'),
	}
	_constraints = [(_check_unique_prog_subs, 'Error: Subsidy Already Exists', ['Subsidy']),(validate_neg_fee_mod, 'Error: % of Module Fee Cannot be Negative', ['Subsidy'])]
program_subsidy()

#Class Program Alerts
###############
class program_alerts(osv.osv):
	def _check_unique_prog_alert(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.program_id == self_obj.program_id and x.program_alert_list == self_obj.program_alert_list:
						return False
		return True
	def on_change_master_program_alerts(self, cr, uid, ids, module_req):
		if not module_req: return {}
		master_req_obj = self.pool.get('master.program.alerts').browse(cr, uid, module_req)
		return {'value': {'time': master_req_obj.time,'befor_after':master_req_obj.befor_after,'min_max':master_req_obj.min_max,
		'value_per':master_req_obj.value_per,'action':master_req_obj.action}}
		
	def create(self,cr, uid, values, context=None):
		module_id = super(program_alerts, self).create(cr, uid, values, context=context)
		line_id=[]
		line_id.append(values['program_alert_list'])
		self.pool.get('master.program.alerts').write(cr, uid, line_id,{'time':values['time'],
		'befor_after':values['befor_after'],'min_max':values['min_max'],'value_per':values['value_per'],'action':values['action']}, context=context)
		return module_id
		
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(program_alerts, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

#Validate Program Alert Time
	def _validate_p_alert_time(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.time < 0:
				return False
		return True

#Validate Program Alert Value		
	def _validate_p_value(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.value_per < 0:
				return False
		return True
		
#Table For Program Alerts
	_name ='program.alert.module'
	_description ="Program Alert Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'alert_id':fields.integer('Id',size=20),
	'program_alert_list':fields.many2one('master.program.alerts', 'Description', ondelete='cascade', help='Description', select=True, required=True),
	'time':fields.float('Time',size=3),
	'befor_after':fields.boolean('Before/After'),
	'min_max':fields.boolean('Min/Max Value'),
	'value_per':fields.integer('Value in %',size=3),
	'action':fields.char('Action',size=100),
	'program_id': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Module'),
	}
	_constraints = [(_check_unique_prog_alert, 'Error: Alert Already Exists', ['Alerts']),(_validate_p_alert_time, 'Error: Alert Time Cannot be Negative', ['Alerts']),(_validate_p_value, 'Error: Alert Value Cannot be Negative', ['Alerts'])]
program_alerts	()

#Class Program Master Alerts
###############
class master_program_alerts(osv.osv):
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
	_name ='master.program.alerts'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Test Descripton',size=20),
	'time':fields.char('Time',size=3),
	'befor_after':fields.boolean('Before/After'),
	'min_max':fields.boolean('Min/Max Value'),
	'value_per':fields.integer('Value in %',size=3),
	'action':fields.char('Action',size=100)
	}
	_constraints = [(_check_unique_name, 'Error: This Alert Already Exists', ['name'])]
master_program_alerts()

#Class Program History
###############
class program_history(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(program_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='program.history.module'
	_description ="Program History Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'history_id':fields.integer('Id',size=20),
	'date_created':fields.char('Date Created',size=20),
	'created_by':fields.char('Created By',size=20),
	'last_update':fields.char('Last Update',size=20),
	'last_update_by':fields.char('Last Update By',size=20),
	'date_status_change':fields.char('Date Of Status Change',size=20),
	'status_change_by':fields.char('Status Change By',size=20),
	'changes':fields.char('Changes',size=200)
	}
program_history	()

####################
#EOF PROGRAMS
####################

####################
#MODULES
####################

#Class CS Module
###############
class cs_module(osv.osv):

#History
    def create(self,cr, uid, values, context=None):
        if 'pre_test' in values and values['pre_test']:
            if len(values['pre_test_line']) == 0:
                raise osv.except_osv(_('Error!'),_("Please add Pre Test"))
        if 'in_class_test' in values and values['in_class_test']:
            if len(values['in_class_test_line']) == 0:
                raise osv.except_osv(_('Error!'),_("Please add In Class Test"))
        if 'post_test' in values and values['post_test']:
            if len(values['post_test_line']) == 0:
                raise osv.except_osv(_('Error!'),_("Please add Post Test"))
        sub_lines = []
        current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
        sub_lines.append( (0,0, {'date_created':fields.date.today(),'created_by':current_user['name'],
             'last_update':'-','last_update_by':'-','date_status_change':fields.date.today(),'status_change_by':current_user['name']}) )
        values.update({'history_line': sub_lines})
        module_id = super(cs_module, self).create(cr, uid, values, context=context)
        return module_id  
    
    def write(self,cr, uid, ids, values, context=None):
        sub_lines = []
        
        current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
        for line in self.browse(cr, uid, ids, context=context):
          history_line_id = self.browse(cr, uid, ids[0], context=context).history_line or []

        num_of_his = len(history_line_id)-1 
        staus_changed_by =   history_line_id[num_of_his]['status_change_by']
        staus_changed_date =   history_line_id[num_of_his]['date_status_change']
 
        if 'module_status' in values:
           staus_changed_date = fields.date.today()
           staus_changed_by  = current_user['name']
           values['date1'] = fields.date.today()
           values['date2'] = fields.date.today()

        
        if 'pre_test' in values and values['pre_test']:
            if 'pre_test_line' in values: 
                if len(values['pre_test_line']) == 0:
                   raise osv.except_osv(_('Error!'),_("Please add Pre Test"))
            else:
                test_line_id =  self.browse(cr, uid, ids[0], context=context).pre_test_line or []
                if len(test_line_id) == 0:
                    raise osv.except_osv(_('Error!'),_("Please add Pre Test"))
        else:
            test_checked =  self.browse(cr, uid, ids[0], context=context).pre_test
            if test_checked :
                if 'pre_test_line' in values: 
                   if len(values['pre_test_line']) == 0:
                       raise osv.except_osv(_('Error!'),_("Please add Pre Test"))
                else:
                   test_line_id =  self.browse(cr, uid, ids[0], context=context).pre_test_line or []
                   if len(test_line_id) == 0:
                       raise osv.except_osv(_('Error!'),_("Please add Pre Test"))
            
        if 'in_class_test' in values and values['in_class_test']:
            if 'in_class_test_line' in values: 
                if len(values['in_class_test_line']) == 0:
                   raise osv.except_osv(_('Error!'),_("Please add In Class Test"))
            else:
                test_line_id =  self.browse(cr, uid, ids[0], context=context).in_class_test_line or []
                if len(test_line_id) == 0:
                    raise osv.except_osv(_('Error!'),_("Please add In Class Test"))
        else:
            test_checked =  self.browse(cr, uid, ids[0], context=context).in_class_test
            if test_checked :
                if 'in_class_test_line' in values: 
                   if len(values['in_class_test_line']) == 0:
                       raise osv.except_osv(_('Error!'),_("Please add In Class Test"))
                else:
                   test_line_id =  self.browse(cr, uid, ids[0], context=context).in_class_test_line or []
                   if len(test_line_id) == 0:
                       raise osv.except_osv(_('Error!'),_("Please add In Class Test"))
     
        if 'post_test' in values and values['post_test']:
            if 'post_test_line' in values: 
                if len(values['post_test_line']) == 0:
                   raise osv.except_osv(_('Error!'),_("Please add Post Test"))
            else:
                test_line_id =  self.browse(cr, uid, ids[0], context=context).post_test_line or []
                if len(test_line_id) == 0:
                    raise osv.except_osv(_('Error!'),_("Please add Post Test"))
        else:
            test_checked =  self.browse(cr, uid, ids[0], context=context).post_test
            if test_checked :
                if 'post_test_line' in values: 
                   if len(values['post_test_line']) == 0:
                       raise osv.except_osv(_('Error!'),_("Please add Post Test"))
                else:
                   test_line_id =  self.browse(cr, uid, ids[0], context=context).post_test_line or []
                   if len(test_line_id) == 0:
                       raise osv.except_osv(_('Error!'),_("Please add Post Test"))
        changes = values.keys()
        module_list ={'name':'Module Name','module_code':'Module Code','module_crscode':'CRS Code','module_certification':'Certification Achieved','module_level':'Level',
           'module_category':'Category','module_pathway':'Pathway','module_credit_value':'Credit Hours','synopsis':'Synopsis','outline':'Outline','module_duration':'Duration',
           'module_fee':'Fee','module_status':'Status','module_center':'Center','description':'Description','delivery_mode':'Delivery Mode','binder_in_use':'Binder',
           'tablet_in_use':'Tablet','primary':'Primary','modalities_in_use':'Modalities In Use','max_num_ppl_class':'Max Number of People in a Class','room_arr':'Room Arrangment',
           'pre_test':'Pre Test Required','in_class_test':'In Class Test Required','post_test':'Post Test Required','module_fee_gst':'Module Fee w/o GST',
           'total_duration':'Total Duration in Hours','min_hr_session':'Minimum Hours Per Session','max_hr_session':'Maximum Hours Per Session',
           'max_session_week':'Maximum Sessions Per Week','req_line':'Requirments','pf_line':'Equipment List','pre_test_line':'Pre Test','in_class_test_line':'In Class',
           'post_test_line':'Post Test','show_do_line':'Show Do','alert_line':'Alerts','show_do_verification':'Verification Required'}
        arr={}
        for i in range(len(changes)):
          if changes[i] in module_list:
             arr[i] = module_list[changes[i]]

        sub_lines.append( (0,0, {'date_created':history_line_id[0]['date_created'],'created_by':history_line_id[0]['created_by'],
             'last_update':fields.date.today(),'last_update_by':current_user['name'],'date_status_change':staus_changed_date,'status_change_by':staus_changed_by,'changes':arr.values()}) )
        values.update({'history_line': sub_lines})
        module_id = super(cs_module, self).write(cr, uid, ids,values, context=context)
        return module_id

#Calculates Module Attributes
    def _calculate_modalities_in_use(self, cr, uid, ids, field_names, args,  context=None):
       if not ids: return {}
       res = {}
       for line in self.browse(cr, uid, ids, context=context):
          module_line = self.browse(cr, uid, ids[0], context=context)
          binder = module_line['binder_in_use']
          tablet = module_line['tablet_in_use']
          modailit_in_use = ''
          if binder:
              modailit_in_use = 'Binder'
          if tablet:
              if modailit_in_use == '':
                 modailit_in_use = 'Tablet'
              else:
                 modailit_in_use += ' and Tablet'
 
       res[line.id] = modailit_in_use
          
       return res 

#Module Status
    def _status_display(self, cr, uid, ids, field_names, args,  context=None):
       if not ids: return {}
       res = {}

       for line in self.browse(cr, uid, ids, context=context):
          res[line.id] = line['module_status']
       return res

    def _status_display_1(self, cr, uid, ids, field_names, args,  context=None):
       if not ids: return {}
       res = {}

       for line in self.browse(cr, uid, ids, context=context):
          res[line.id] = line['module_status']
       return res
	   
#Module Fee
    def on_change_module_fee_gst(self, cr, uid, ids, module_fee_gst):
       return {'value': {'module_fee': module_fee_gst}}
 
#Validate Module Fee
    def _check_neg_fee(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.module_fee < 0:
                return False
        return True

#Module Duration
    def on_change_module_duration_inside(self, cr, uid, ids, total_duration):
       return {'value': {'module_duration': total_duration}}

#Validate Module Duration
    def _check_neg_duration(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.module_duration < 0:
                return False
        return True

    def on_change_req_line(self, cr, uid, ids, module_duration):
       return {'value': {'req_line': req_dropdown}}
	   
#Module Desc 
    def on_change_module_desc(self, cr, uid, ids, description):
       return {'value': {'synopsis': description}}

#Module Synopsis 
    def on_change_module_synopsis(self, cr, uid, ids, synopsis):
       return {'value': {'description': synopsis}}

    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        
        res = super(cs_module, self).read(cr, uid,ids, fields, context, load)
        seq_number =0 
        for r in res:
        	seq_number = seq_number+1
        	r['s_no'] = seq_number
        
        return res

#Validate Module Name
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
		
#Validate Module Code
    def _check_unique_code(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        lst = [
                x.module_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
                if x.module_code and x.id not in ids
              ]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.module_code and self_obj.module_code.lower() in  lst:
               return False
        return True

#To show Status in  Popup
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

#Validate Max no. of People				
    def _check_neg_no_ppl(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.max_num_ppl_class < 0:
                return False
        return True

#Validate Credit Value
    def _check_neg_credit_value(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 ,[], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.module_credit_value < 0:
                return False
        return True

#Table For cs Modules		
    _name = "cs.module"
    _description = "Modules"
    _columns = {
       'program_id': fields.integer('Id',size=20),
	   's_no': fields.integer('S.No',size=20),
       'name': fields.char('Module Name', size=128, required=True, select=True),
       'module_code': fields.char('Module Code', size=20),
	   'module_crscode': fields.char('CRS Code', size=20),
	   'module_certification': fields.char('Certification Achieved (if any)', size=100),
	   'module_level': fields.selection((('L1','L1'),('L2','L2'),('L3','L3'),('L4','L4'),('L5','L5')),'Level'),
	   'module_category': fields.selection((('WPL','WPL'),('WPN','WPN'),('WPS','WPS'),('EDGE','EDGE'),('LPM','LPM'),('SV','SV'),('Non WSQ','Non WSQ')),'Category'),
	   'module_pathway': fields.selection((('Generic','Generic'),('Sectorial','Sectorial'),('Contextualized','Contextualized')),'Pathway'),
	   'module_credit_value': fields.integer('Credit Hours', size=4),
	   'orientation': fields.selection((('Yes','Yes'),('No','No')),'Orientation'),
	   'synopsis':fields.text('Synopsis', size=100),
	   'outline':fields.text('Outline', size=100),
	   'module_duration': fields.float('Duration in hours', size=4),
	   'module_fee': fields.float('Fee $',size=9),
	   'module_status': fields.selection((('Incomplete','Incomplete'),('Active','Active'),('InActive','InActive'),('Completed','Completed')),'Status', required=True, select=True),
	   'module_center': fields.selection((('Hougang','Hougang'),('Jurong','Jurong'),('Tampines','Tampines'),('Woodlands','Woodlands')),'Select Center'),
	   'select_program': fields.selection((('Program 1','Program 1'),('Program 2','Program 2'),('Program 3','Program 3'),('Program 4','Program 4')),'Select Program'),
	   'description': fields.text('Description', size=500),
	   'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
	   'binder_in_use':fields.boolean('Binder'),
	   'tablet_in_use':fields.boolean('Tablet'),
	   'primary': fields.selection((('Binder','Binder'),('Tablet','Tablet'),('Blended','Blended')),'Primary'),
	   'modalities_in_use' : fields.function(_calculate_modalities_in_use, relation="cs.module",string='Modalities In Use',readonly=1,type='char',store=True),
	   'max_num_ppl_class': fields.integer('Max Number of People in a Class', size=3),
	   'room_arr': fields.selection((('Default','Default'),('Active','Active')),'Room Arrangment'),
	   'pre_test': fields.boolean('Pre Test Required'),
	   'in_class_test': fields.boolean('In Class Test Required'),
	   'post_test': fields.boolean('Post Test Required'),
	   'module_fee_gst': fields.float('Module Fee w/o GST'),
	   'total_duration': fields.integer('Total Duration in Hours'),
	   'min_hr_session': fields.integer('Minimum Hours Per Session'),
	   'max_hr_session': fields.integer('Maximum Hours Per Session'),
	   'max_session_week': fields.integer('Maximum Sessions Per Week'),
	   'req_line': fields.one2many('req.module','mod_id','Requirments'),
	   'pf_line': fields.one2many('pf.module','mod_id','Equipment List'),
	   'pre_test_line': fields.one2many('pre.test.module','mod_id','Pre Test'),
	   'in_class_test_line': fields.one2many('in.class.test.module','mod_id','In Class'),
	   'post_test_line': fields.one2many('post.test.module','mod_id','Post Test'),
	   'show_do_line': fields.one2many('show.do.module','mod_id','Show Do'),
	   'alert_line': fields.one2many('alert.module','mod_id','Alerts', type='integer'),
	   'history_line': fields.one2many('history.module','mod_id','History', limit=None),
	   'status_display': fields.function(_status_display, readonly=1, type='char'),
	   'status_display_1': fields.function(_status_display_1, readonly=1, type='char'),
	   'date1': fields.date('Date Created', readonly='True'),
	   'date2': fields.date('Date Created', readonly='True'),
	   'show_status':fields.boolean("Show Status"),
	   'show_do_item':fields.char('Item', size=20),
	   'show_do_verification':fields.boolean("Verification Required"),
	   'limit': fields.integer('Limit', help='Default limit for the list view'),
	   'no_of_alerts': fields.integer('No. of Alerts'),
	   'program_modules': fields.one2many('program.modules','s_no', 'Modules'),
	   'no_of_modules': fields.integer('No. of Modules',size=1),
	   'Module1_group': fields.one2many('test.module.group1', 's_no'),
	   'Module2_group': fields.one2many('test.module.group2', 's_no'),
	   'Module3_group': fields.one2many('test.module.group3', 's_no'),
	   'Module4_group': fields.one2many('test.module.group4', 's_no'),
	   'group_name1': fields.char('Group Name'),
	   'group_name2': fields.char('Group Name'),
	   'group_name3': fields.char('Group Name'),
	   'group_name4': fields.char('Group Name'),
	   'max_modules1': fields.integer('Max Modules'),
	   'max_modules2': fields.integer('Max Modules'),
	   'max_modules3': fields.integer('Max Modules'),
	   'max_modules4': fields.integer('Max Modules'),
    }
    _defaults = { 
	   'date1': fields.date.context_today,
	   'date2': fields.date.context_today,
	   'limit': 5,
	   'module_duration': 0.00,
	   'orientation': 'No',
    }
    _order='name'
    _constraints = [(_check_unique_name, 'Error: Module Name Already Exists', ['Module Name']),(_check_unique_code, 'Error: Module Code Already Exists', ['Module Code']),(_check_neg_duration, 'Error: Duration Cannot be negative value', ['Duration']),(_check_neg_fee, 'Error: Fee Cannot be negative value', ['Fee']),(_check_neg_credit_value, 'Error: Credit Value Cannot be negative', ['Credit']),(_check_neg_no_ppl, 'Error: No. of People Cannot be negative value', ['People'])]

cs_module()

#Class Module Requirements
###############
class requirments(osv.osv):
	def _check_unique_req(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.master_req == self_obj.master_req:
						return False
		return True
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('req.module')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['mod_id'].id)
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

	def on_change_master_req(self, cr, uid, ids, module_req):
		if not module_req: return {}
		master_req_obj = self.pool.get('master.req').browse(cr, uid, module_req)
		return {'value': {'description': master_req_obj.description,'musthave':master_req_obj.musthave,'verification':master_req_obj.verification}}
		
	def create(self,cr, uid, values, context=None):
		module_id = super(requirments, self).create(cr, uid, values, context=context)
		line_id=[]
		line_id.append(values['master_req'])
		self.pool.get('master.req').write(cr, uid, line_id,{'description':values['description'],
		'musthave':values['musthave'],'verification':values['verification']}, context=context)
		return module_id
		
	_name ='req.module'
	_description ="Requirement Tab"
	_rec_name='mod_id'
	_columns = {
	#'req_id':fields.integer('S.No',size=20),
	'master_req':fields.many2one('master.req', 'Label', ondelete='cascade', help='Requirements', select=True,required=True),
	'description':fields.char('Description',size=20),
	'musthave':fields.boolean('Must Have'),
	'verification':fields.boolean('Verification'),
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	'module_name': fields.related('mod_id','name',type="char",relation="cs.module",string="Module Name"),
	'module_code': fields.related('mod_id','module_code',type="char",relation="cs.module",string="Module Code"),
	}
	_constraints = [(_check_unique_req, 'Error: Requirement Already Exists', ['Requirement'])]
requirments()

#Class Module Master Requirements
###############
class master_req(osv.osv):
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
	_name ='master.req'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Label',size=20,required=True),
	'description':fields.char('Description',size=100),
	'musthave':fields.boolean('Must Have'),
	'verification':fields.boolean('Verification'),
	}
	_constraints = [(_check_unique_name, 'Error: Requirement Label Already Exists', ['name'])]
master_req()

#Class Module Master Equipment
###############
class master_equip(osv.osv):
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
	_name ='master.equip'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Equipment',size=20),
	}
	_constraints = [(_check_unique_name, 'Error: This Equipment Already Exists', ['name'])]
master_equip()   

#Class Module Master Test
###############
class master_tests(osv.osv):
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
	_name ='master.tests'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Test Descripton',size=20),
	}
	_constraints = [(_check_unique_name, 'Error: This Description Already Exists', ['name'])]
master_tests()

#Class Module MOI
###############
class peoplefac(osv.osv):
	def _check_unique_equp(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.equip_list == self_obj.equip_list:
						return False
		return True
	_name ='pf.module'
	_description ="People and Facilites Tab"
	_columns = {
	'pf_id':fields.integer('S.No',size=20),
	'equip_list':fields.many2one('master.equip', 'Equipment', ondelete='cascade', help='Equipments', select=True,required=True),
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	}
	_constraints = [(_check_unique_equp, 'Error: Equipment Already Exists', ['Equipment'])]
peoplefac()

#Class Module Pre Test
###############
class pre_test(osv.osv):
	def _check_unique_pre_test(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.test_list == self_obj.test_list:
						return False
		return True
	def unlink(self, cr, uid, ids, context=None):
		mod_id = self.browse(cr, uid, ids[0], context=context).mod_id
		test_checked =  self.pool.get('cs.module').browse(cr, uid, mod_id.id, context=context).pre_test
		if test_checked:
			sr_ids = super(pre_test, self).search(cr, uid, [('mod_id', '=', mod_id.id)],context=context)
			final_val = len(sr_ids) - len(ids)
			if final_val == 0: 
				raise osv.except_osv(_('Error!'),_("Atleast One Pre Test Required"))
		return super(pre_test, self).unlink(cr, uid, ids, context=context)
	def _check_unique_order(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.order_priority == self_obj.order_priority:
						return False
		return True
		
#Validate Order of Preority
	def _check_neg_order_priority(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.order_priority < 0:
				return False
		return True

#Table for Test in Modules
	_name ='pre.test.module'
	_description ="Pre Test Table"
	_columns = {
	#'pre_test_id':fields.integer('Order Of Priority',size=20),
	'order_priority':fields.integer('Order Of Priority',size=2,required=True),
	'test_list':fields.many2one('master.tests', 'Test Description', ondelete='cascade', help='Description', required=True),
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	}
	_constraints = [(_check_unique_pre_test, 'Error: Test Already Exists', ['Test']),
     (_check_unique_order, 'Error: Order Id Should Be Unique', ['Order']),
     (_check_neg_order_priority, 'Error: Order of Priority Cannot be negative value', ['Order'])]
pre_test()

#Class Module In Class
###############
class in_class_test(osv.osv):
	def unlink(self, cr, uid, ids, context=None):
		mod_id = self.browse(cr, uid, ids[0], context=context).mod_id
		test_checked =  self.pool.get('cs.module').browse(cr, uid, mod_id.id, context=context).in_class_test
		if test_checked:
			sr_ids = super(in_class_test, self).search(cr, uid, [('mod_id', '=', mod_id.id)],context=context)
			final_val = len(sr_ids) - len(ids)
			if final_val == 0: 
				raise osv.except_osv(_('Error!'),_("Atleast One In Class Test Required"))
		return super(in_class_test, self).unlink(cr, uid, ids, context=context)
	def _check_unique_in_class_test(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.test_list == self_obj.test_list:
						return False
		return True

	def _check_unique_order(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.order_priority == self_obj.order_priority:
						return False
		return True
		
#Validate Order of Preority
	def _check_neg_order_priority(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.order_priority < 0:
				return False
		return True
	_name ='in.class.test.module'
	_description ="In Calss Table"
	_columns = {
	#'in_class_id':fields.integer('Order Of Priority',size=20),
	'order_priority':fields.integer('Order Of Priority',size=2,required=True),
	'test_list':fields.many2one('master.tests', 'Test Description', ondelete='cascade', help='Description', select=True, required=True),
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	}
	_constraints = [(_check_unique_in_class_test, 'Error: In Class Test Already Exists', ['test_list']),
     (_check_unique_order, 'Error: Order Id Should Be Unique', ['Order']),
     (_check_neg_order_priority, 'Error: Order of Priority Cannot be negative value', ['Order'])]
in_class_test()

#Class Module Post Test
###############
class post_test(osv.osv):
	def unlink(self, cr, uid, ids, context=None):
		mod_id = self.browse(cr, uid, ids[0], context=context).mod_id
		test_checked =  self.pool.get('cs.module').browse(cr, uid, mod_id.id, context=context).post_test
		if test_checked:
			sr_ids = super(post_test, self).search(cr, uid, [('mod_id', '=', mod_id.id)],context=context)
			final_val = len(sr_ids) - len(ids)
			if final_val == 0: 
				raise osv.except_osv(_('Error!'),_("Atleast One Post Test Required"))
		return super(post_test, self).unlink(cr, uid, ids, context=context)
	def _check_unique_post_test(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.test_list == self_obj.test_list:
						return False
		return True
		
	def _check_unique_order(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.order_priority == self_obj.order_priority:
						return False
		return True
#Validate Order of Preority
	def _check_neg_order_priority(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.order_priority < 0:
				return False
		return True
	_name ='post.test.module'
	_description ="Post Test Table"
	_columns = {
	#'post_test_id':fields.integer('Order Of Priority',size=20),
	'order_priority':fields.integer('Order Of Priority',size=2,required=True),
	'test_list':fields.many2one('master.tests', 'Test Description', ondelete='cascade', help='Description', select=True, required=True),
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	}
	_constraints = [(_check_unique_post_test, 'Error: Post Test Already Exists', ['test_list']),
     (_check_unique_order, 'Error: Order Id Should Be Unique', ['Order']),
     (_check_neg_order_priority, 'Error: Order of Priority Cannot be negative value', ['Order'])]
post_test()

#Class Module Master Alerts
###############
class master_alerts(osv.osv):
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
	_name ='master.module.alerts'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Test Descripton',size=20),
	'time':fields.char('Time',size=3),
	'befor_after':fields.boolean('Before/After'),
	'min_max':fields.boolean('Min/Max Value'),
	'value_per':fields.integer('Value in %',size=3),
	'action':fields.char('Action',size=100)
	}
	_constraints = [(_check_unique_name, 'Error: This Alert Description Already Exists', ['name'])]
master_alerts()

#Class Module Alert
###############
class alerts(osv.osv):
	def _check_unique_alert(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.alert_list == self_obj.alert_list:
						return False
		return True
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(alerts, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

#Validate Module Alert Time
	def _validate_m_alert_time(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.time < 0:
				return False
		return True

#Validate Module Alert Value		
	def _validate_m_value(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.value_per < 0:
				return False
		return True
				
	def on_change_master_module_alerts(self, cr, uid, ids, module_req,mod_id):
		if not module_req: return {}
		master_req_obj = self.pool.get('master.module.alerts').browse(cr, uid, module_req)
		
		return {'value': {'time': master_req_obj.time,'befor_after':master_req_obj.befor_after,'min_max':master_req_obj.min_max,
		'value_per':master_req_obj.value_per,'action':master_req_obj.action}}
		
	def create(self,cr, uid, values, context=None):
		module_id = super(alerts, self).create(cr, uid, values, context=context)
		line_id=[]
		line_id.append(values['alert_list'])
		self.pool.get('master.module.alerts').write(cr, uid, line_id,{'time':values['time'],
		'befor_after':values['befor_after'],'min_max':values['min_max'],'value_per':values['value_per'],'action':values['action']}, context=context)
		return module_id
	_name ='alert.module'
	_description ="Alert Tab"
	_columns = {
	'alert_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'alert_list':fields.many2one('master.module.alerts', 'Description', ondelete='cascade', help='Description', select=True,required=True),
	'time':fields.float('Time',size=3),
	'befor_after':fields.boolean('Before/After'),
	'min_max':fields.boolean('Min/Max Value'),
	'value_per':fields.integer('Value in %',size=3),
	'action':fields.char('Action',size=100),
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module'),
	}
	_constraints = [(_check_unique_alert, 'Error: Alert Already Exists', ['Alerts']),(_validate_m_alert_time, 'Error: Alert Time Cannot be Negative', ['Alerts']),(_validate_m_value, 'Error: Alert Value Cannot be Negative', ['Alerts'])]
alerts()

#Class Module History
###############
class history(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='history.module'
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
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	'changes':fields.char('Changes',size=200)
	}
history	()

####################
#EOF MODULES
####################

######################################### ASZ Technologies asztechnologies.com ##################################
