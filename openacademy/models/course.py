# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Course(models.Model):
    # Modelo course de la base de datos
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
