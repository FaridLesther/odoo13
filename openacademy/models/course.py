# -*- coding: utf-8 -*-
# modelos para tablas de la base de datos
from odoo import models, fields, api


class Course(models.Model):
    #n
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
