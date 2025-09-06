{
    "name": "АРМ Оператора",
    "version": "18.0",
    "category": "Производство мебели",
    "summary": "Автоматизированное рабочее место оператора",
    "description": """
        Модуль для автоматизации рабочего места оператора.
        
        Основные функции:
        - Управление производственными заданиями
        - Отслеживание статусов выполнения
        - Интерфейс для операторов станков
        - Авторизация операторов
        - Отчеты по производительности
        
        Уровни реализации:
        easy: базовый интерфейс АРМ с возможностью отмечать задания
        medium: полноценная логика работы с заданиями, улучшенный интерфейс
        hard: система операторов и авторизация
    """,
    "author": "alexanderdryomov7@gmail.com",
    "website": "https://www.test_proj_asai-arm.com",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "security/groups.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/task_views.xml",
        "views/menu_views.xml",
        "wizard/defect_reason_wizard_views.xml",
        "data/demo_data.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": True,
}
