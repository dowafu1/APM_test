from odoo import models, fields, api

class WorkAssignment(models.Model):
    _name = 'work.assignment'
    _description = 'Задание для оператора'

    name = fields.Char(string='Название задания', required=True)
    status = fields.Selection([
        ('ready', 'Готово к работе'),
        ('in_progress', 'В работе'),
        ('done', 'Готово'),
        ('defect', 'Брак')
    ], string='Статус', default='ready')
    start_time = fields.Datetime(string='Время начала')
    end_time = fields.Datetime(string='Время окончания')
    description = fields.Text(string='Описание')

    def action_take_to_work(self):
        self.write({
            'status': 'in_progress',
            'start_time': fields.Datetime.now()
        })

    def action_mark_done(self):
        self.write({
            'status': 'done',
            'end_time': fields.Datetime.now()
        })

    def action_mark_defect(self):
        self.write({
            'status': 'defect',
            'end_time': fields.Datetime.now()
        })