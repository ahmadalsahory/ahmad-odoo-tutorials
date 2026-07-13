{
    'name': 'To-Do Application',
    'version': '1.0',
    'summary': 'Manage to-do tasks and assign them to users.',
    'category': 'Tools',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_task_view.xml',
        'views/base_menu.xml',
    ],
    'installable': True,
    'application': True,
}
