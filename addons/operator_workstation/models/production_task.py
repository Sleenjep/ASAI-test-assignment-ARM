from odoo import models, fields

class ProductionTask(models.Model):
    _name = 'production.task'
    _description = 'Производственное задание'

    name = fields.Char('Номер задания', required=True)
    part_name = fields.Char('Название детали', required=True)
    operation = fields.Selection([
        ('cutting', 'Раскрой'),
        ('edging', 'Кромка'),
        ('drilling', 'Присадка'),
        ('packaging', 'Упаковка'),
    ], string='Операция', required=True)
    
    state = fields.Selection([
        ('ready', 'Готово к работе'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнено'),
        ('defect', 'Брак'),
    ], string='Статус', default='ready')
    
    start_time = fields.Datetime('Время начала')
    end_time = fields.Datetime('Время окончания')
    
    def action_take_in_work(self):
        self.state = 'in_progress'
        self.start_time = fields.Datetime.now()
        return True
    
    def action_mark_done(self):
        self.state = 'done'
        self.end_time = fields.Datetime.now()
        return True
    
    def action_mark_defect(self):
        self.state = 'defect'
        self.end_time = fields.Datetime.now()
        return True