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

from openerp.osv import fields, osv

    
class project_lifecycle(osv.osv):
    
    _name = "project.lifecycle"
    _description = 'Lifecycle Stage'
    _order = 'sequence'
    
    _columns = {        
        'name': fields.char('Stage Name', size=32, required=True, translate=True),
        'sequence': fields.integer('Sequence'),                                  
    }

    _defaults = {
        'sequence': 1
    }    


project_lifecycle()

