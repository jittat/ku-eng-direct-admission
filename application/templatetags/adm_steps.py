from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('application/tags/form_steps.html',
                        takes_context=True)
def form_steps(context, step_list=None, current_step=0, max_linked_step=0):
    if 'form_step_info' in context:
        form_step_info = context['form_step_info']

        if 'steps' in form_step_info:
            step_list = form_step_info['steps']
        if step_list == None:
            step_list = []

        if 'current_step' in form_step_info:
            current_step = form_step_info['current_step']
        
        if 'max_linked_step' in form_step_info:
            max_linked_step = form_step_info['max_linked_step']
    
    # build step information

    print max_linked_step

    steps = []
    i = 0
    for s in step_list:
        step_info = {
            'text': s[0],
            'url': reverse(s[1]),
            'is_current': False,
            'is_clickable': False
            }

        if i==current_step:
            step_info['is_current'] = True
        elif i<=max_linked_step:
            step_info['is_clickable'] = True

        steps.append(step_info)
        i += 1
    return { 'steps' : steps }
