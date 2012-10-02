# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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

import tools
from osv import fields, osv
from tools.translate import _

    
class project(osv.osv):
   
    _inherit = "project.project"
 
    def set_draft(self, cr, uid, ids, *args, **kwargs):
        res = super(project, self).set_draft(cr, uid, ids, *args, **kwargs)
        projects = self.browse(cr, uid, ids)
        self._history(cr, uid, projects, _('Draft'))
        return res
    
    def set_open(self, cr, uid, ids, *args, **kwargs):
        res = super(project, self).set_open(cr, uid, ids, *args, **kwargs)
        projects = self.browse(cr, uid, ids)
        self._history(cr, uid, projects, _('Open'))
        return res
    
    def set_pending(self, cr, uid, ids, *args, **kwargs):
        res = super(project, self).set_pending(cr, uid, ids, *args, **kwargs)
        projects = self.browse(cr, uid, ids)
        self._history(cr, uid, projects, _('Pending'))
        return res
    
    def set_done(self, cr, uid, ids, *args, **kwargs):
        res = super(project, self).set_done(cr, uid, ids, *args, **kwargs)
        projects = self.browse(cr, uid, ids)
        self._history(cr, uid, projects, _('Done'))
        return res
    
    def set_cancel(self, cr, uid, ids, *args, **kwargs):
        res = super(project, self).set_cancel(cr, uid, ids, *args, **kwargs)
        projects = self.browse(cr, uid, ids)
        self._history(cr, uid, projects, _('Cancel'))
        return res   


project()

