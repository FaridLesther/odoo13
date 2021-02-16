# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _


class Course(models.Model):
    # Modelo course de la base de datos
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Titulo", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsable", index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sesiones")

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]


    