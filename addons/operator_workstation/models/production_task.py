from odoo import models, fields, api, exceptions
from datetime import datetime


class ProductionTask(models.Model):
    _name = "production.task"
    _description = "Производственное задание"
    _order = "priority desc, sequence, create_date"

    name = fields.Char("Номер задания", required=True)
    part_name = fields.Char("Название детали", required=True)
    operation = fields.Selection(
        [
            ("cutting", "Раскрой"),
            ("edging", "Кромка"),
            ("drilling", "Присадка"),
            ("packaging", "Упаковка"),
        ],
        string="Операция",
        required=True,
    )

    state = fields.Selection(
        [
            ("ready", "Готово к работе"),
            ("in_progress", "В работе"),
            ("done", "Выполнено"),
            ("defect", "Брак"),
        ],
        string="Статус",
        default="ready",
    )

    start_time = fields.Datetime("Время начала")
    end_time = fields.Datetime("Время окончания")
    duration = fields.Float(
        "Длительность (в минутах)", compute="_compute_duration", store=True
    )

    operator_id = fields.Many2one("res.users", string="Оператор", readonly=True)

    priority = fields.Selection(
        [
            ("0", "Низкий"),
            ("1", "Нормальный"),
            ("2", "Высокий"),
            ("3", "Критический"),
        ],
        string="Приоритет",
        default="1",
    )

    sequence = fields.Integer("Последовательность", default=10)

    notes = fields.Text("Примечания")
    description = fields.Text("Описание задания")

    quantity = fields.Integer("Количество", default=1)
    material = fields.Char("Материал")
    dimensions = fields.Char("Размеры")

    # брак
    defect_reason = fields.Text("Причина брака")

    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        """Подсчёт времени выполнения задания"""
        for record in self:
            if record.start_time and record.end_time:
                delta = record.end_time - record.start_time
                record.duration = delta.total_seconds() / 60.0
            else:
                record.duration = 0.0

    def action_take_in_work(self):
        """Взять задание в работу"""
        for record in self:
            if record.state != "ready":
                raise exceptions.UserError(
                    'Можно взять в работу только задания со статусом "Готово к работе"'
                )

            in_progress_tasks = self.search(
                [("operator_id", "=", self.env.user.id), ("state", "=", "in_progress")]
            )
            if in_progress_tasks and record.id not in in_progress_tasks.ids:
                raise exceptions.UserError(
                    "У вас уже есть задание в работе. Завершите его перед тем, как взять новое."
                )

            record.write(
                {
                    "state": "in_progress",
                    "start_time": fields.Datetime.now(),
                    "operator_id": self.env.user.id,
                }
            )
        return True

    def action_mark_done(self):
        """Отметить задание как выполненное"""
        for record in self:
            if record.state != "in_progress":
                raise exceptions.UserError("Можно завершить только задания в работе")
            if record.operator_id != self.env.user:
                raise exceptions.UserError("Вы можете завершить только свои задания")

            record.write({"state": "done", "end_time": fields.Datetime.now()})
        return True

    def action_mark_defect(self):
        """Отметить задание как брак с указанием причины"""
        for record in self:
            if record.state != "in_progress":
                raise exceptions.UserError(
                    "Можно отправить в брак только задания в работе"
                )
            if record.operator_id != self.env.user:
                raise exceptions.UserError(
                    "Вы можете отправить в брак только свои задания"
                )

        return {
            "type": "ir.actions.act_window",
            "name": "Указать причину брака",
            "res_model": "defect.reason.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_task_id": self.id,
            },
        }

    def action_return_to_ready(self):
        """Вернуть задание в статус "Готово к работе" """
        for record in self:
            if record.state not in ["in_progress", "defect"]:
                raise exceptions.UserError(
                    "Можно вернуть в работу только задания в работе или браке"
                )
            if record.operator_id != self.env.user:
                raise exceptions.UserError(
                    "Вы можете вернуть в работу только свои задания"
                )

            record.write(
                {
                    "state": "ready",
                    "start_time": False,
                    "end_time": False,
                    "operator_id": False,
                }
            )
        return True
