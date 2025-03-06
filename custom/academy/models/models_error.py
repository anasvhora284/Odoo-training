# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Teachers(models.Model):
    _name = 'academy.teachers'
    _description = 'Academy Teachers'

    name = fields.Char()
    biography = fields.Html()
    course_ids = fields.One2many('product.template', 'teacher_id', string="Courses")

class Courses(models.Model):
    _name = 'academy.courses'
    _description = 'Academy Courses'
    _inherit = ['product.template', 'mail.thread']

    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")