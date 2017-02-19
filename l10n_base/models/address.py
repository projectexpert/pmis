# -*- encoding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _


class ResRegion(models.Model):
    _name = 'res.region'
    _description = 'Region'

    name = fields.Char(
        'Region Name', size=64, help='The full name of the region.',
        required=True
    )
    country_id = fields.Many2one(
        'res.country', 'Country', ondelete='restrict'
    )

    _order = "name"


class ResProvince(models.Model):
    _name = 'res.province'
    _description = 'Province'

    @api.one
    def name_get(self):
        if self.code and self._context.get('province_code', False):
            return (
                self.id, "(" + self.code + ")"
            )
        else:
            return (
                self.id, self.name
            )

    name = fields.Char(
        'Province Name', size=64, help='The full name of the province.',
        required=True
    )
    code = fields.Char(
        'Province Code', size=6, help='The province code in two chars.',
        required=True
    )
    region = fields.Many2one('res.region', 'Region', ondelete='restrict')

    _order = "name"


class ResCity(models.Model):
    _name = 'res.city'
    _description = 'City'

    name = fields.Char('City', size=64, required=True)
    province_id = fields.Many2one(
        'res.province', 'Province', ondelete='restrict'
    )
    zip = fields.Char('ZIP', size=5)
    phone_prefix = fields.Char(_('Telephone Prefix'), size=16)
    istat_code = fields.Char(_('ISTAT code'), size=16)
    cadaster_code = fields.Char(_('Cadaster Code'), size=16)
    web_site = fields.Char(_('Web Site'), size=64)
    region = fields.Many2one(
        related='province_id.region', string=_('Region'), readonly=True
    )

    _order = "name"


class Address(models.AbstractModel):
    _name = 'base.address'

    @api.one
    def check_category(self):
        countries = self.env['res.country'].search(
            [('name', '=', self.country_id.name)]
        )
        if countries:
            country = countries[0]
            self.enable_province = country.enable_province
            self.enable_region = country.enable_region
            self.enable_state = country.enable_state
        else:
            self.enable_province = False
            self.enable_region = False
            self.enable_state = False

    @api.one
    def dummy(self):
        self.auto_off = False

    province = fields.Many2one(
        'res.province', string='Province', ondelete='restrict'
    )
    region = fields.Many2one(
        'res.region', string='Region', ondelete='restrict'
    )
    find_city = fields.Boolean('Find City')
    enable_province = fields.Boolean(
        compute=check_category, string='Provinces?', readonly=True
    )
    enable_region = fields.Boolean(
        compute=check_category, string='Regions?', readonly=True
    )
    enable_state = fields.Boolean(
        compute=check_category, string='States?', readonly=True, default=True
    )
    auto_off = fields.Boolean(
        compute=dummy, string=_('Auto off'), help="Unlock address fields"
    )

    _defaults = {
        'type': 'default',
    }

    def address_autocomplete(self, city):
        self.province = city.province_id and city.province_id.id or False
        self.region = city.region and city.region.id or False
        self.country_id = (
            city.region.country_id and
            city.region.country_id.id or
            False
        )
        self.city = city.name
        self.find_city = True

        self.enable_province = city.region.country_id.enable_province
        self.enable_region = city.region.country_id.enable_region
        self.enable_state = city.region.country_id.enable_state

    @api.one
    @api.onchange('zip')
    def on_change_zip(self):
        if self.zip and len(self.zip) > 3:
            city = self.env['res.city']
            city_ids = city.search([('zip', '=ilike', self.zip)])
            if not city_ids:
                city_ids = city.search(
                    [('zip', '=ilike', self.zip[:3] + 'xx')]
                )

            if len(city_ids) == 1:
                city = city_ids[0]

                self.address_autocomplete(city)

    @api.one
    @api.onchange('city')
    def on_change_city(self):
        if self.city:
            cities = self.env['res.city'].search(
                [('name', '=ilike', self.city.title())]
            )
            if cities:
                city = cities[0]
                if not self.zip:
                    self.zip = city.zip

                self.address_autocomplete(city)

    @api.one
    @api.onchange('country_id')
    def on_change_country(self):
        if self.country_id:
            self.enable_province = self.country_id.enable_province
            self.enable_region = self.country_id.enable_region
            self.enable_state = self.country_id.enable_state

    @api.one
    @api.onchange('province')
    def on_change_province(self):
        if self.province:
            self.region = (
                self.province.region and
                self.province.region.id or
                False
            )

    @api.one
    @api.onchange('region')
    def on_change_region(self):
        if self.region:
            self.country_id = (
                self.region.country_id and
                self.region.country_id.id or
                False
            )

    def _set_vals_city_data(self, vals):
        if 'city' in vals and 'province' not in vals and 'region' not in vals:
            if vals['city']:
                cities = self.env['res.city'].search(
                    [('name', '=ilike', vals['city'].title())]
                )
                if cities:
                    city = cities[0]
                    if 'zip' not in vals:
                        vals['zip'] = city.zip
                    if city.province_id:
                        vals['province'] = city.province_id.id
                    if city.region:
                        vals['region'] = city.region.id
                        if city.region.country_id:
                            vals['country_id'] = city.region.country_id.id
        return vals

    @api.model
    def create(self, vals):
        if 'auto_off' in vals and not vals['auto_off'] or 'auto_off' \
                not in vals:
            vals = self._set_vals_city_data(vals)
        return super(Address, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'auto_off' in vals and not vals['auto_off'] or 'auto_off' \
                not in vals:
            vals = self._set_vals_city_data(vals)
        return super(Address, self).write(vals)
