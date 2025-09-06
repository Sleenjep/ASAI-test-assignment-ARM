from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields


class TestProductionTask(TransactionCase):

    def setUp(self):
        super(TestProductionTask, self).setUp()

        self.operator_group = self.env.ref("operator_workstation.group_operator")

        self.operator = self.env["res.users"].create(
            {
                "name": "Тестовый оператор",
                "login": "test_operator",
                "email": "operator@some.com",
                "groups_id": [(4, self.operator_group.id)],
            }
        )

        self.task = self.env["production.task"].create(
            {
                "name": "ТЗ-001",
                "part_name": "Тестовая деталь",
                "operation": "cutting",
                "quantity": 1,
                "material": "Дуб",
                "dimensions": "100x100x18",
            }
        )

    def test_task_creation(self):
        """Тест создания задания"""
        self.assertEqual(self.task.state, "ready")
        self.assertEqual(self.task.name, "ТЗ-001")
        self.assertEqual(self.task.operation, "cutting")
        self.assertFalse(self.task.operator_id)

    def test_take_in_work(self):
        """Тест взятия задания в работу"""
        self.task = self.task.with_user(self.operator)

        self.task.action_take_in_work()

        self.assertEqual(self.task.state, "in_progress")
        self.assertEqual(self.task.operator_id, self.operator)
        self.assertTrue(self.task.start_time)

    def test_cannot_take_non_ready_task(self):
        """Тест, что нельзя взять задание не в статусе 'ready'"""
        self.task.state = "done"

        with self.assertRaises(UserError):
            self.task.action_take_in_work()

    def test_cannot_take_multiple_tasks(self):
        """Тест, что нельзя взять несколько заданий одновременно"""
        task2 = self.env["production.task"].create(
            {
                "name": "ТЗ-002",
                "part_name": "Тестовая деталь 2",
                "operation": "cutting",
            }
        )

        self.task = self.task.with_user(self.operator)
        task2 = task2.with_user(self.operator)

        self.task.action_take_in_work()

        with self.assertRaises(UserError):
            task2.action_take_in_work()

    def test_mark_done(self):
        """Тест завершения задания"""
        self.task = self.task.with_user(self.operator)
        self.task.action_take_in_work()

        self.task.action_mark_done()

        self.assertEqual(self.task.state, "done")
        self.assertTrue(self.task.end_time)

    def test_mark_defect(self):
        """Тест отправки задания в брак"""
        self.task = self.task.with_user(self.operator)
        self.task.action_take_in_work()

        result = self.task.action_mark_defect()

        self.assertEqual(result["res_model"], "defect.reason.wizard")
        self.assertEqual(result["view_mode"], "form")
        self.assertEqual(result["target"], "new")

    def test_cannot_finish_others_task(self):
        """Тест, что нельзя завершить чужое задание"""
        operator2 = self.env["res.users"].create(
            {
                "name": "Второй оператор",
                "login": "test_operator2",
                "email": "operator2@test.com",
                "groups_id": [(4, self.operator_group.id)],
            }
        )

        self.task = self.task.with_user(self.operator)
        self.task.action_take_in_work()

        self.task = self.task.with_user(operator2)
        with self.assertRaises(UserError):
            self.task.action_mark_done()

    def test_duration_calculation(self):
        """Тест расчета длительности выполнения"""
        self.task = self.task.with_user(self.operator)

        start_time = fields.Datetime.from_string("2023-01-01 10:00:00")
        end_time = fields.Datetime.from_string("2023-01-01 12:30:00")

        self.task.write(
            {
                "start_time": start_time,
                "end_time": end_time,
            }
        )

        self.assertEqual(self.task.duration, 150.0)

    def test_return_to_ready(self):
        """Тест возврата задания в статус готово к работе"""
        self.task = self.task.with_user(self.operator)
        self.task.action_take_in_work()
        self.task.action_mark_defect()

        self.task.action_return_to_ready()

        self.assertEqual(self.task.state, "ready")
        self.assertFalse(self.task.start_time)
        self.assertFalse(self.task.end_time)
        self.assertFalse(self.task.operator_id)
