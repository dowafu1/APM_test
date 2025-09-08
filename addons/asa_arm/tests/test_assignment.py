from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import AccessError

class TestWorkAssignment(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_operator = cls.env['res.users'].create({
            'name': 'Оператор Тестовый',
            'login': 'operator_test',
            'email': 'operator@example.com',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])]
        })
        
        # Получаем модель задания
        cls.Assignment = cls.env['work.assignment'].with_user(cls.user_operator)

    def test_01_create_assignment(self):
        assignment = self.Assignment.create({
            'name': 'Тестовое задание 1',
            'description': 'Описание тестового задания'
        })
        self.assertTrue(assignment.id, "Задание не было создано")
        self.assertEqual(assignment.status, 'ready', "Неверный статус по умолчанию")
        self.assertFalse(assignment.start_time, "Время начала не должно быть заполнено")
        self.assertFalse(assignment.end_time, "Время окончания не должно быть заполнено")

    def test_02_take_to_work(self):
        assignment = self.Assignment.create({
            'name': 'Тестовое задание 2'
        })
        
        # Сохраняем время до действия
        time_before = fields.Datetime.now()
        
        # Выполняем действие
        assignment.action_take_to_work()
        
        # Проверяем результаты
        self.assertEqual(assignment.status, 'in_progress', "Статус должен быть 'in_progress'")
        self.assertIsNotNone(assignment.start_time, "Время начала должно быть заполнено")
        # Проверяем, что время начала примерно соответствует времени вызова метода
        self.assertGreaterEqual(assignment.start_time, time_before, "Время начала должно быть >= времени до действия")

    def test_03_mark_done(self):
        assignment = self.Assignment.create({
            'name': 'Тестовое задание 3'
        })
        assignment.action_take_to_work()
        time_before_done = fields.Datetime.now()
        
        assignment.action_mark_done()
        
        self.assertEqual(assignment.status, 'done', "Статус должен быть 'done'")
        self.assertIsNotNone(assignment.end_time, "Время окончания должно быть заполнено")
        self.assertGreaterEqual(assignment.end_time, time_before_done, "Время окончания должно быть >= времени до действия")

    def test_04_mark_defect(self):
        assignment = self.Assignment.create({
            'name': 'Тестовое задание 4'
        })
        assignment.action_take_to_work()
        time_before_defect = fields.Datetime.now()
        
        assignment.action_mark_defect()
        
        self.assertEqual(assignment.status, 'defect', "Статус должен быть 'defect'")
        self.assertIsNotNone(assignment.end_time, "Время окончания должно быть заполнено")
        self.assertGreaterEqual(assignment.end_time, time_before_defect, "Время окончания должно быть >= времени до действия")

    def test_05_access_rights(self):
        admin_assignment = self.env['work.assignment'].create({
            'name': 'Тестовое задание 5 (админ)'
        })

        try:
            operator_assignment = self.Assignment.browse(admin_assignment.id)
            self.assertEqual(operator_assignment.name, 'Тестовое задание 5 (админ)', "Оператор должен видеть задание")
        except AccessError:
            self.fail("Оператор не должен получить AccessError при чтении задания")
