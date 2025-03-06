# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Teachers(models.Model):
    _name = 'academy.teachers'
    _description = 'Academy Teachers'

    name = fields.Char()
    biography = fields.Html()
    course_ids = fields.One2many('academy.courses', 'teacher_id', string="Courses")

class Courses(models.Model):
    _name = 'academy.courses'
    _description = 'Academy Courses'
    _inherit = ['product.template']

    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")

    taxes_id = fields.Many2many('account.tax', 'course_taxes_rel', 'prod_id', 'tax_id',
        string="Sales Taxes",
        help="Default taxes used when selling the product",
        domain=[('type_tax_use', '=', 'sale')],
        default=lambda self: self.env.company.account_sale_tax_id or self.env.company.root_id.sudo().account_sale_tax_id,
    )
    supplier_taxes_id = fields.Many2many('account.tax', 'course_supplier_taxes_rel', 'prod_id', 'tax_id',
        string="Purchase Taxes",
        help="Default taxes used when buying the product",
        domain=[('type_tax_use', '=', 'purchase')],
        default=lambda self: self.env.company.account_purchase_tax_id or self.env.company.root_id.sudo().account_purchase_tax_id,
    )
    optional_product_ids = fields.Many2many(
        comodel_name='product.template',
        relation='course_optional_rel',
        column1='src_id',
        column2='dest_id',
        string="Optional Products",
        help="Optional Products are suggested "
             "whenever the customer hits *Add to Cart* (cross-sell strategy, "
             "e.g. for computers: warranty, software, etc.).",
        check_company=True)
    alternative_product_ids = fields.Many2many(
        string="Alternative Products",
        comodel_name='product.template',
        relation='course_alternative_rel',
        column1='src_id', column2='dest_id',
        check_company=True,
        help="Suggest alternatives to your customer (upsell strategy)."
             " Those products show up on the product page.",
    )
    accessory_product_ids = fields.Many2many(
        string="Accessory Products",
        comodel_name='product.template',
        relation='course_accessory_rel',
        column1='src_id', column2='dest_id',
        check_company=True,
        help="Accessories show up when the customer reviews the cart before payment"
             " (cross-sell strategy).",
    )
