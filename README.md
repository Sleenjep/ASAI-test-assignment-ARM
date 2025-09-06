# АРМ Оператора - Тестовое задание АСАИ

> **Автоматизированное рабочее место оператора** для системы производственного учета мебельных производств на базе Odoo 18.0

# Google-drive с демонстрацией проделанной работы:

> **GDrive:** https://drive.google.com/drive/folders/1e8xRQb3UNAAWxknVX0G2e827QZM6nM-t?usp=sharing

## Быстрый старт

```bash
    git clone https://github.com/Sleenjep/ASAI-test-assignment-ARM.git
    cd ASAI-test-assignment-ARM
    docker-compose up
```

## О проекте

Данный модуль разработан в рамках тестового задания для компании АСАИ - системы производственного учета с фокусом на мебельные производства (MES блок ERP системы).

**Проблема**: Большинство мебельщиков не устраивают существующие на рынке продукты, многим приходится вести учет в Excel.

**Решение**: АРМ Оператора - ключевой модуль для автоматизации работы линейных сотрудников на производстве.

### Используемый технологии:

- **Backend**: Odoo 18.0 (Python 3.11+)
- **Frontend**: Odoo Web Client (JavaScript/XML/CSS)
- **Database**: PostgreSQL 15
- **Frontend**: Odoo Web Client (JavaScript/XML/CSS)
- **Контейнеризация**: Docker + Docker Compose
- **Web-сервер**: Werkzeug (встроенный в Odoo)
- **Линтер для python**: Black

### Пошаговая установка

1. Подготовка окружения

```bash
    git clone https://github.com/Sleenjep/ASAI-test-assignment-ARM.git
    cd ASAI-test-assignment-ARM
```

2. Первый запуск (инициализация)

```bash
    docker-compose up
```

При повторном запуске docker-compose следует закомментировать строчку:

```yml
    command: ["odoo", "--config=/etc/odoo/odoo.conf", "-i", "base,operator_workstation"] # инициализация БД
```

и раскомментировать, соответственно

```yml
    command: ["odoo", "--config=/etc/odoo/odoo.conf"] # при повторном запуске docker-compose.yml
```

4. Доступ к системе
- **URL**: http://localhost:8069
- **База данных**: postgres_odoo_db
- **Пользователи**: администратор и два оператора

### Предустановленные пользователи

| Логин | Пароль | Роль | Описание |
|-------------|--------|------|----------|
| admin | admin | Администратор | Полный доступ к системе |
| ivan | ivan | Оператор | Иван Иванов - оператор #1 |
| petr | petr | Оператор | Петр Петров - оператор #2 |


### Меню системы

**Для операторов:**
- `Мои задания` - активные задания оператора
- `Выполненные задания` - архив завершенных работ

**Для администратора:**
- `АРМ Оператора` - все задания в системе
- Полный доступ к настройкам и управлению

## Модели данных

**Основная модель производственного задания**

```python
    class ProductionTask(models.Model):
        _name = 'production.task'
        _description = 'Производственное задание'
        _order = 'priority desc, sequence, create_date'
```

**Структура полей:**

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | Char | Номер задания |
| `part_name` | Char | Название детали |
| `operation` | Selection | Тип операции |
| `state` | Selection | Статус задания |
| `priority` | Selection | Приоритет (0-3) |
| `quantity` | Integer | Количество изделий |
| `material` | Char | Материал |
| `dimensions` | Char | Размеры |
| `operator_id` | Many2one | Назначенный оператор |
| `start_time` | Datetime | Время начала |
| `end_time` | Datetime | Время окончания |
| `duration` | Float | Длительность (мин) |
| `description` | Text | Описание |
| `notes` | Text | Примечания |
| `defect_reason` | Text | Причина брака |

## Безопасность и права доступа

### Группы пользователей

**1. Оператор производства (`group_operator`)**
- Просмотр только своих заданий и свободных
- Взятие заданий в работу
- Завершение и отправка в брак
- Нет прав на создание/удаление

**2. Администратор производства (`group_production_manager`)**
- Полный доступ ко всем заданиям
- Создание и управление заданиями
- Контроль работы операторов
- Системное администрирование

## Тестирование

**Тестовые сценарии:**

```python
class TestProductionTask(TransactionCase):
    
    def test_task_creation(self):
        """Проверка создания задания"""
        
    def test_take_in_work(self):
        """Взятие задания в работу"""
        
    def test_cannot_take_multiple_tasks(self):
        """Нельзя взять несколько заданий"""
        
    def test_mark_done(self):
        """Завершение задания"""
        
    def test_mark_defect(self):
        """Отправка в брак"""
        
    def test_duration_calculation(self):
        """Расчет длительности"""
```

### Запуск тестов

**Полный цикл тестирования:**

```bash
    docker-compose run --rm web odoo \
    --config=/etc/odoo/odoo.conf \
    --test-enable \
    --stop-after-init \
    --log-level=test \
    -d postgres_odoo_db \
    --update operator_workstation
```

**Только выполнение тестов:**

```bash
    docker-compose run --rm web odoo \
    --config=/etc/odoo/odoo.conf \
    --test-enable \
    --stop-after-init \
    --log-level=test \
    -d postgres_odoo_db \
    --test-tags operator_workstation
```
