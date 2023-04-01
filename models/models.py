import datetime
from collections import defaultdict
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.tools import date_utils, float_round, float_is_zero


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('patient_default_code', 'unique(default_code)', 'Internal Reference  must be unique !'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if not vals.get('barcode'):
                seq_date = None
                if 'company_id' in vals:
                    vals['barcode'] = self.env['ir.sequence'].with_context(
                        force_company=vals['company_id']).next_by_code(
                        'product.template', sequence_date=seq_date) or _('New')
                else:
                    vals['barcode'] = self.env['ir.sequence'].next_by_code(
                        'product.template', sequence_date=seq_date) or _('New')
                related_vals['barcode'] = vals['barcode']
            if related_vals:
                template.write(related_vals)
        return templates


class ProductProduct(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [
        ('patient_default_code', 'unique(default_code)', 'Internal Reference  must be unique !'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self).create(vals_list)
        for product, vals in zip(products, vals_list):
            related_vals = {}
            if not vals.get('barcode'):
                seq_date = None
                if 'company_id' in vals:
                    vals['barcode'] = self.env['ir.sequence'].with_context(
                        force_company=vals['company_id']).next_by_code(
                        'product.product', sequence_date=seq_date) or _('New')
                else:
                    vals['barcode'] = self.env['ir.sequence'].next_by_code(
                        'product.product', sequence_date=seq_date) or _('New')
                related_vals['barcode'] = vals['barcode']
                if related_vals:
                    product.write(related_vals)
        return products


