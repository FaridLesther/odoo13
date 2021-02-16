# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(string="Nombre", required=True)
    start_date = fields.Date(string="Fecha Inicio", default=fields.Date.today)
    duration = fields.Float(string="Duración", digits=(6, 2), help="Duración en días")
    seats = fields.Integer(string="Número de plazas")
    active = fields.Boolean(string="Activo", default=True)
    color = fields.Integer()

    instructor_id = fields.Many2one('res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])

    course_id = fields.Many2one('openacademy.course',
        ondelete='cascade', string="Curso", required=True)

    attendee_ids = fields.Many2many('res.partner', string="Participantes")

    #Campos calculados
    taken_seats = fields.Float(string="Plazas ocupadas", compute='_taken_seats')
    end_date = fields.Date(string="Fecha fin", store=True, compute='_get_end_date', inverse='_set_end_date')

    attendees_count = fields.Integer(string="Número de Participantes", compute='_get_attendees_count', store=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
    
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Valor de plazas incorrecto"),
                    'message': _("El número disponible de plazas no puede ser negativo"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Hay más Participantes que plazas disponibles"),
                    'message': _("Incremente las plazas o borre el exceso de Participantes"),
                },
            }

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Agregue duración a start_date, pero: Lunes + 5 días = Sábado, entonces 
            # reste un segundo para obtener el viernes en su lugar
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Calcule la diferencia entre fechas, pero: viernes - lunes = 4 días,
            # así que agregue un día para obtener 5 días en su lugar
            r.duration = (r.end_date - r.start_date).days + 1
    
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError(_("Un instructor de sesión no puede ser un participante"))