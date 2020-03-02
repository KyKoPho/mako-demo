import os
import traceback

from jinja2 import Environment, FileSystemLoader
import mako
from mako import exceptions
from mako.lookup import TemplateLookup

def render():
        template_path = os.getcwd()

        jinja_env = Environment(loader=FileSystemLoader([template_path]), autoescape=True)

        mako_template_lookup = TemplateLookup(directories=[template_path])
        
        for template in get_templates():
    
            template_type = template[0]
            template_file = template[1]
            data_func = template[2]
               
            if template_type == 'j':
                template = jinja_env.get_template(template_file)
                try:
                    output = template.render(data_func())
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print("Exception %s", e)

            elif template_type == 'm':
                template = mako_template_lookup.get_template(template_file)
                try:
                    output = template.render(data=get_mako_data(), format_exceptions=True)
                except:
                    output = exceptions.html_error_template().render().decode('utf-8')
            
            with open('out-' + template_file, 'w+') as outfile:
                outfile.write(output)
                outfile.close()

def get_templates():
    return [
        # ('j', 'jinja.html', get_jinja_data),
        # ('m', 'mako.html', get_mako_data),
        # ('j', 'jinja-if.html', get_jinja_data),
        # ('m', 'mako-if.html', get_mako_data),
        # ('j', 'jinja-complicated-data.html', get_complicated_data_jinja),
        ('m', 'mako-complicated-data.html', get_complicated_data_mako),
    ]

class SlimShady:
    name = None
    data = dict()

    def __init__(self, name, data=None):
        self.name = name
        self.data = data

def get_mako_data():
    return [SlimShady('SLIM SHADY') for _ in range(10)]

def get_jinja_data():
    return {'data': [SlimShady('SLIM SHADY')  for _ in range(10)]}

def get_complicated_data_jinja():
    return { 
        'data' : 
            SlimShady('Kyland', {
                'level_one': [{
                        'level_two': {
                            'level_three': 'SLIM SHADY'
                        }
                    }]
                })
        }

def get_complicated_data_mako():
    return SlimShady('Kyland', {
                    'level_one': [{
                            'level_two': {
                                'level_three': 'SLIM SHADY'
                            }
                        }]
                    })