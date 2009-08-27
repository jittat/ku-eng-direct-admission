from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('application/tags/form_steps.html',
                        takes_context=True)
def form_steps(context, step_list=None, current_step=0):
    if 'steps' in context:
        step_list = context['steps']
    if step_list == None:
        step_list = []
    if 'current_step' in context:
        current_step = context['current_step']
    
    # build step information

    steps = []
    i = 0
    for s in step_list:
        step_info = {
            'text': s[0],
            'url': reverse(s[1]),
            'is_current': False 
            }
        if i==current_step:
            step_info['is_current'] = True
        steps.append(step_info)
        i += 1
    return { 'steps' : steps }
