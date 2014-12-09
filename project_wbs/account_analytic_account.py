# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv


class account_analytic_account(osv.osv):
    
    _inherit = 'account.analytic.account'

    def get_child_accounts(self, cr, uid, ids, context=None):    
        result = {}
        read_data = []
        read_data = self.pool.get('account.analytic.account').read(cr, uid, ids,['child_ids'])
        for data in read_data:                
            for curr_id in ids:
                result[curr_id] = True   
            for child_id in data['child_ids']:  
                lchild_id = []
                lchild_id.append(child_id)                                                         
                result.update(self.get_child_accounts(cr, uid, lchild_id, context))         
        return result

    def _complete_wbs_code_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):        
        if not ids:
            return []
        res = []    
        for account in self.browse(cr, uid, ids, context=None):    
            data = []
            acc = account             
            while acc:
                if acc.code:
                    data.insert(0, acc.code)
                else:
                    data.insert(0,'')                    
                
                acc = acc.parent_id
            data = ' / '.join(data)
            data = '[' + data + '] '   
            
            res.append((account.id, data))
        return dict(res)                                 

    def _complete_wbs_name_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):        
        if not ids:
            return []
        res = []    
        for account in self.browse(cr, uid, ids, context=None):    
            data = []
            acc = account             
            while acc:
                if acc.name:
                    data.insert(0, acc.name)
                else:
                    data.insert(0,'')                    

                acc = acc.parent_id
                
            data = ' / '.join(data)
            res.append((account.id, data))
        return dict(res)

    def _child_count(self, cr, uid, ids, account_class, arg, context=None):
        if context is None:
            context = {}
        res = dict.fromkeys(ids, 0)
        ctx = context.copy()
        ctx['active_test'] = False
        for analytic_account in self.browse(cr, uid, ids, context=context):
            deliverable_ids = self.pool.get('account.analytic.account').search(cr, uid,
                                                                      [('parent_id', '=', analytic_account.id),
                                                                       ('account_class', '=', account_class)],
                                                                      context=ctx)
            if deliverable_ids:
                res[analytic_account.id] = len(deliverable_ids)
            else:
                res[analytic_account.id] = 0

        return res

    def _child_project_count(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        return self._child_count(cr, uid, ids, 'project', arg, context=context)

    def _child_phase_count(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        return self._child_count(cr, uid, ids, 'phase', arg, context=context)

    def _child_deliverable_count(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        return self._child_count(cr, uid, ids, 'deliverable', arg, context=context)

    def _child_work_package_count(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        return self._child_count(cr, uid, ids, 'work_package', arg, context=context)

    def _child_unclassified_count(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        return self._child_count(cr, uid, ids, '', arg, context=context)

    def _resolve_analytic_account_id_from_context(self, cr, uid, context=None):
        """ Returns ID of parent analytic account based on the value of 'default_parent_id'
            context key, or None if it cannot be resolved to a single
            account.analytic.account
        """
        if context is None:
            context = {}
        if type(context.get('default_parent_id')) in (int, long):
            return context['default_parent_id']
        if isinstance(context.get('default_parent_id'), basestring):
            analytic_account_name = context['default_parent_id']
            analytic_account_ids = self.pool.get('account.analytic.account').name_search(cr, uid,
                                                                                         name=analytic_account_name,
                                                                                         context=context)
            if len(analytic_account_ids) == 1:
                return analytic_account_ids[0][0]
        return None

    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('analytic.account.stage')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        analytic_account_id = self._resolve_analytic_account_id_from_context(cr, uid, context=context)
        if analytic_account_id:
            search_domain += ['|', ('analytic_account_ids', '=', analytic_account_id)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(cr, uid, search_domain, order=order,
                                      access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        fold = {}
        for stage in stage_obj.browse(cr, access_rights_uid, stage_ids, context=context):
            fold[stage.id] = stage.fold or False
        return result, fold

    _columns = {
        'complete_wbs_code': fields.function(_complete_wbs_code_calc, method=True, type='char',
                                             string='Full WBS Code', size=250,
                                             help='The full WBS code describes the full path of this '
                                                  'component within the project WBS hierarchy',
                                             store={
                                                 'account.analytic.account': (get_child_accounts,
                                                                              ['name', 'code', 'parent_id'], 20)
                                            }),

        'complete_wbs_name': fields.function(_complete_wbs_name_calc, method=True, type='char',
                                             string='Full WBS path', size=250,
                                             help='Full path in the WBS hierarchy',
                                             store={'account.analytic.account': (get_child_accounts,
                                                                                  ['name', 'code', 'parent_id'], 20)
                                                    }),

        'account_class': fields.selection([('project', 'Project'), ('phase', 'Phase'),
                                           ('deliverable', 'Deliverable'),
                                           ('work_package','Work Package')], 'Class',
                                          help='The classification allows you to create a proper project '
                                               'Work Breakdown Structure'),
        'stage_id': fields.many2one('analytic.account.stage', 'Stage', track_visibility='onchange',
                                    domain="['&', ('fold', '=', False), ('analytic_account_ids', '=', parent_id)]"),
        'child_stage_ids': fields.many2many('analytic.account.stage', 'analytic_account_stage_rel',
                                      'analytic_account_id', 'stage_id', 'Child Stages',
                                      states={'close': [('readonly', True)], 'cancelled': [('readonly', True)]}),
        'child_project_count': fields.function(_child_project_count, type='integer', string="Projects"),
        'child_phase_count': fields.function(_child_phase_count, type='integer', string="Phases"),
        'child_deliverable_count': fields.function(_child_deliverable_count, type='integer', string="Deliverables"),
        'child_work_package_count': fields.function(_child_work_package_count, type='integer', string="Work Packages"),
        'child_unclassified_count': fields.function(_child_unclassified_count, type='integer',
                                                    string="Unclassified projects"),
    }

    def _get_type_common(self, cr, uid, context):
        ids = self.pool.get('analytic.account.stage').search(cr, uid, [('case_default','=',1)], context=context)
        return ids

    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }

    _defaults = {
        'child_stage_ids': _get_type_common,
    }

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):        
        if not args:
            args = []
        if context is None:
            context = {}
        
        args = args[:]
        accountbycode = self.search(cr, uid, [('complete_wbs_code', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)        
        accountbyname = self.search(cr, uid, [('complete_wbs_name', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
        account = accountbycode + accountbyname

        return self.name_get(cr, uid, account, context=context)
    
    def code_get(self, cr, uid, ids, context=None):

        if not ids:
            return []
        res = []
        for account in self.browse(cr, uid, ids, context=context):
            data = []
            acc = account
            while acc:
                if acc.code:
                    data.insert(0, acc.code)
                else:
                    data.insert(0, '')
                
                acc = acc.parent_id
            data = ' / '.join(data)
            res.append((account.id, data))
        return res

    def name_get(self, cr, uid, ids, context=None):        

        if not ids:
            return []
        if type(ids) is int:ids = [ids]

        new_list = []
        for i in ids:
            if i not in new_list:
                new_list.append(i)
        ids = new_list

        res = []
        for account in self.browse(cr, uid, ids, context=context):
            data = []
            acc = account
            while acc:
                if acc.name:
                    data.insert(0, acc.name)
                else:
                    data.insert(0, '')
                acc = acc.parent_id
                
            data = ' / '.join(data)
            res2 = self.code_get(cr, uid, [account.id], context=None)
            if res2:
                data = '[' + res2[0][1] + '] ' + data            

            res.append((account.id, data))
        return res


account_analytic_account()