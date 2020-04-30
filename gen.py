#!/usr/bin/env python

from datetime import date
import os

import json
import yaml

def translate_type(type):
    if type == 'string':
        return 'String'
    elif type == 'integer':
        return 'Int'
    else:
        return '<# ? #>'

def parse_parameters(parameters):
    formatted = []

    for parameter in parameters:
        if not parameter['in'] == 'path':
            continue

        stripped = {}
        stripped['name'] = to_camel_case(parameter['name'])
        stripped['type'] = translate_type(parameter['schema']['type'])
        formatted.append(stripped['name'] + ': '+stripped['type'])

    return ', '.join(formatted)

def strip_data(spec):
    stripped = []

    for path, path_data in spec['paths'].items():
        for method, details in path_data.items():
            tags = details['tags']

            # to skip unwanted routes, play here.
            # if not 'tag' in tags:
            #     continue

            summary = details['summary']
            data = {}

            # you'll have to update the index here, too.
            data['route'] = tags[0]
            data['method'] = method
            data['description'] = details['summary'].capitalize()
            # replace any path info here.
            data['path'] = path.replace('', '')

            try:
                data['parameters'] = parse_parameters(details['parameters'])
            except KeyError:
                pass

            stripped.append(data)

    return stripped

def sort_into_routes(data):
    routes = {}
    for path in data:
        if path['route'] in routes:
            routes[path['route']].append(path)
        else:
            routes[path['route']] = [path]

    return routes

def gen_header(spec, header_template, file):
    settings = yaml.safe_load(open('./settings.yml', 'r'))

    d = {}
    d['file'] = file
    d['project'] = settings['project']
    d['organization'] = settings['organization']
    d['title'] = spec['info']['title']
    d['version'] = spec['info']['version']
    d['date'] = date.today().strftime('%Y-%m-%d')
    d['year'] = date.today().strftime('%Y')

    return header_template.format(**d)

def gen_endpoint(path):
    endpoint_template = open('./templates/endpoint.txt').read()

    d = {}
    if 'parameters' in path:
        d['parameters'] = path['parameters']
    else:
        d['parameters'] = ''
    d['method'] = path['method']
    d['path'] = path['path'].replace('{', '\(').replace('}', ')')

    return endpoint_template.format(**d)

def gen_docs(path):
    pass

def generate_route_files(spec, file_header_template, output_path, routes):
    try:
        os.mkdir(f'{output_path}API')
    except:
        pass

    for route, paths in routes.items():
        header = gen_header(spec, file_header_template, route)
        route_caps = route.capitalize().replace(' ', '')

        file = open(f'{output_path}API/{route_caps}.swift', 'w')
        file.write(header+'\n')
        file.write('import Foundation\n\n')
        file.write(f'extension API {{\n    enum {route_caps} {{}}\n}}\n\n')
        file.write(f'extension API.{route_caps} {{ \n\n')

        for path in paths:
            # docs = gen_docs(path)
            # file.write(docs)
            endpoint = gen_endpoint(path)
            description = path['description']
            file.write(f'    /// {description}\n')
            file.write(endpoint + '\n')

            path = path['path']
            # print(f'Generated endpoint for {path}...')

        file.write('}')
        file.close()

def copy_file(spec, file_header_template, output_path, name):
    file = open(f'{output_path}{name}.swift', 'w')
    header = gen_header(spec, file_header_template, 'API')
    file.write(header+'\n')
    file.write(open(f'./templates/swift/{name}.swift').read())
    file.close()

def main():
    settings = yaml.safe_load(open('./settings.yml', 'r'))

    spec = json.load(open(settings['spec']))
    file_header_template = open('./templates/file_header.txt').read()
    func_docs_template = open('./templates/function_documentation.txt').read()

    title = spec['info']['title']
    version = spec['info']['version']

    output_path = f'./output/{title}_v{version}/'

    try:
        os.mkdir(output_path)
    except OSError:
        pass

    data = strip_data(spec)
    routes = sort_into_routes(data)

    copy_file(spec, file_header_template, output_path, 'API')
    copy_file(spec, file_header_template, output_path, 'Client')
    copy_file(spec, file_header_template, output_path, 'Endpoint')

    generate_route_files(spec, file_header_template, output_path, routes)
    
    new_path = output_path.replace('./', '')
    print(f'Wrapper can be found in {new_path}')

# https://stackoverflow.com/a/19053800
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

if __name__ == "__main__":
    main()
