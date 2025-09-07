{
    'name': 'АСАИ – Тестовое задание – АРМ',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Автоматизированное рабочее место оператора',
    'description': """
        Модуль для отслеживания заданий операторов на мебельном производстве.
    """,
    'author': 'Dowafu',
    'depends': ['base'],
    'data': [
        'views/assignment_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}