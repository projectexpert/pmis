# -*- encoding: utf-8 -*-

def post_init(cr, registry):
    """Import CSV data as it is faster than xml and because we can't use
    noupdate with csv"""
    from openerp.tools import convert_file
    filename = 'data_it/res.city.csv'
    convert_file(
        cr, 'l10n_base_data_it', filename, None, mode='init',
        noupdate=True, kind='init', report=None
    )
