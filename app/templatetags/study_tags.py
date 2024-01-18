from django import template

register = template.Library()

@register.filter(name='status_to_string')
def convert_status_to_string(status, name):
    print(f'name = {name}')
    if status == 10:
        return 'Success'
    elif status == 20:
        return 'Pending'
    elif status == 30:
        return 'Error'
    elif status == 40:
        return 'Failed'
    else:
        'Unknown'