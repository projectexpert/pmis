# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010-2013 Didotech Srl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.osv import fields
from openerp.tools.translate import _
from collections import defaultdict
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class res_region(orm.Model):
    _name = 'res.region'
    _description = 'Region'
    _columns = {
        'name': fields.char(
            'Region Name', size=64,
            help='The full name of the region.', required=True
        ),
        'country_id': fields.many2one(
            'res.country', 'Country', ondelete='restrict'
        ),
    }
    _order = "name"


class res_province(orm.Model):
    _name = 'res.province'
    _description = 'Province'

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for province in self.read(
            cr, uid, ids, ['code', 'name'], context=context
        ):
            if province['code'] and context.get('province_code', False):
                name = "(" + province['code'] + ")"
            else:
                name = province['name']
            res.append((province['id'], name))
        return res

    _columns = {
        'name': fields.char(
            'Province Name', size=64,
            help='The full name of the province.', required=True
        ),
        'code': fields.char(
            'Province Code', size=6,
            help='The province code in two chars.', required=True
        ),
        'region': fields.many2one(
            'res.region', 'Region', ondelete='restrict'
        ),
    }
    _order = "name"


class res_city(orm.Model):
    _name = 'res.city'
    _description = 'City'

    _columns = {
        'name': fields.char('City', size=64, required=True),
        'province_id': fields.many2one(
            'res.province', 'Province', ondelete='restrict'
        ),
        'zip': fields.char('ZIP', size=5),
        'phone_prefix': fields.char('Telephone Prefix', size=16),
        'istat_code': fields.char('ISTAT code', size=16),
        'cadaster_code': fields.char('Cadaster Code', size=16),
        'web_site': fields.char('Web Site', size=64),
        'region': fields.related(
            'province_id', 'region', type='many2one',
            relation='res.region', string='Region', readonly=True
        ),
    }
    _order = "name"


class res_partner(orm.Model):
    _inherit = 'res.partner'

    def check_category(self, cr, uid, ids, field_names, arg, context):
        result = {}
        country_obj = self.pool.get('res.country')

        for streetaddress in self.browse(cr, uid, ids):
            country_ids = country_obj.search(
                cr, uid, [('name', '=', streetaddress.country_id.name)]
            )
            if country_ids:
                countries = country_obj.browse(cr, uid, country_ids)
                for country in countries:
                    for field_name in field_names:
                        if streetaddress.id not in result:
                            result[streetaddress.id] = {}

                        if getattr(country, field_name):
                            result[streetaddress.id][field_name] = False
                        elif not result[streetaddress.id].get(
                            field_name, False
                        ):
                            result[streetaddress.id][field_name] = True
            else:
                for field_name in field_names:
                    if streetaddress.id not in result:
                        result[streetaddress.id] = {}
                    result[streetaddress.id][field_name] = False

        return result

    def dummy(self, cr, uid, ids, field_names, arg, context):
        return defaultdict(bool)

    _columns = {
        'province': fields.many2one(
            'res.province', string='Province', ondelete='restrict'
        ),
        'region': fields.many2one(
            'res.region', string='Region', ondelete='restrict'
        ),
        'find_city': fields.boolean('Find City'),
        'enable_province': fields.function(
            check_category, string='Provinces?', type='boolean',
            readonly=True, method=True, multi=True
        ),
        'enable_region': fields.function(
            check_category, string='Regions?', type='boolean',
            readonly=True, method=True, multi=True
        ),
        'enable_state': fields.function(
            check_category, string='States?', type='boolean',
            readonly=True, method=True, multi=True, default=True
        ),
        'auto_off': fields.function(
            dummy, string=_('Auto off'), type='boolean',
            help="Unlock address fields"
        )
    }

    _defaults = {
        'type': 'default',
    }

    def on_change_zip(self, cr, uid, ids, zip_code):
        res = {'value': {}}

        if zip_code and len(zip_code) > 3:
            city_obj = self.pool['res.city']
            city_ids = city_obj.search(cr, uid, [('zip', '=ilike', zip_code)])
            if not city_ids:
                city_ids = city_obj.search(
                    cr, uid, [('zip', '=ilike', zip_code[:3] + 'xx')]
                )

            if len(city_ids) == 1:
                city_obj = self.pool['res.city'].browse(cr, uid, city_ids[0])
                res = {'value': {
                    'province': (
                        city_obj.province_id and
                        city_obj.province_id.id or
                        False
                    ),
                    'region': (
                        city_obj.region and
                        city_obj.region.id or
                        False
                    ),
                    'country_id': (
                        city_obj.region.country_id and
                        city_obj.region.country_id.id or
                        False
                    ),
                    'city': city_obj.name,
                    'find_city': True,
                }}
        return res

    def on_change_city(self, cr, uid, ids, city, zip_code=None):
        res = {'value': {'find_city': False}}
        if city:
            city_obj = self.pool['res.city']
            city_ids = city_obj.search(
                cr, uid, [('name', '=ilike', city.title())]
            )
            if city_ids:
                city_row = city_obj.browse(cr, uid, city_ids[0])
                if zip_code:
                    zip_code = zip_code
                else:
                    zip_code = city_row.zip

                res = {'value': {
                    'province': (
                        city_row.province_id and
                        city_row.province_id.id or
                        False
                    ),
                    'region': (
                        city_row.region and
                        city_row.region.id or
                        False
                    ),
                    'zip': zip_code,

                    'country_id': (
                        city_row.region and
                        city_row.region.country_id and
                        city_row.region.country_id.id or
                        False
                    ),

                    'city': city.title(),
                    'find_city': True,
                }}
        return res

    def on_change_province(self, cr, uid, ids, province):
        res = {'value': {}}
        if province:
            province_obj = self.pool['res.province'].browse(cr, uid, province)
            res = {
                'value': {
                    'region': (
                        province_obj.region and
                        province_obj.region.id or
                        False
                    )
                }
            }
        return res

    def on_change_region(self, cr, uid, ids, region):
        res = {'value': {}}
        if region:
            region_obj = self.pool['res.region'].browse(cr, uid, region)
            res = {
                'value': {
                    'country_id': (
                        region_obj.country_id and
                        region_obj.country_id.id or
                        False
                    )
                }
            }
        return res

    def _set_vals_city_data(self, cr, uid, vals):
        if 'city' in vals and 'province' not in vals and 'region' not in vals:
            if vals['city']:
                city_obj = self.pool['res.city']
                city_ids = city_obj.search(
                    cr,
                    uid,
                    [
                        (
                            'name',
                            '=ilike',
                            vals['city'].title()
                        )
                    ]
                )
                if city_ids:
                    city = city_obj.browse(cr, uid, city_ids[0])
                    if 'zip' not in vals:
                        vals['zip'] = city.zip
                    if city.province_id:
                        vals['province'] = city.province_id.id
                    if city.region:
                        vals['region'] = city.region.id
                        if city.region.country_id:
                            vals['country_id'] = city.region.country_id.id
        return vals

    def create(self, cr, uid, vals, context=None):
        if (
            'auto_off' in vals and not vals['auto_off'] or
                'auto_off' not in vals
        ):
            vals = self._set_vals_city_data(cr, uid, vals)
        return super(res_partner, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        if (
            'auto_off' in vals and not vals['auto_off'] or
                'auto_off' not in vals
        ):
            vals = self._set_vals_city_data(cr, uid, vals)
        return super(res_partner, self).write(cr, uid, ids, vals, context)
