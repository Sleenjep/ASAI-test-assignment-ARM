{
    'name': 'АРМ Оператора',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Автоматизированное рабочее место оператора',
    'description': """
        Модуль для автоматизации рабочего места оператора производственного участка.
        
        Основные функции:
        - Управление производственными заданиями
        - Отслеживание статусов выполнения
        - Интерфейс для операторов станков
    """,
    'author': 'alexanderdryomov7@gmail.com',
    'website': 'https://www.asai-arm.com',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/task_views.xml',
        'views/menu_views.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}