from odoo import models, fields, api


class DefectReasonWizard(models.TransientModel):
    _name = "defect.reason.wizard"
    _description = "Мастер указания причины брака"

    defect_reason = fields.Text("Причина брака", required=True)
    task_id = fields.Many2one("production.task", string="Задание")

    def confirm_defect(self):
        """Подтвердить брак с указанием причины"""
        if self.task_id:
            self.task_id.write(
                {
                    "state": "defect",
                    "end_time": fields.Datetime.now(),
                    "defect_reason": self.defect_reason,
                }
            )
        return {"type": "ir.actions.act_window_close"}
