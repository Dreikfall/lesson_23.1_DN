import os
from utils import iterator, filter_query, filter_map, filter_unique, filter_sort, filter_limit
from flask import Flask, request, abort
from exceptions import FilterMapColErrors

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query")
def perform_query():
    req_arg = request.args
    if not req_arg.get('file_name'):
        abort(404)
    try:
        data_iter = iterator(f"data/{req_arg.get('file_name')}")
    except FileNotFoundError:
        return 'Файла не существует'
    if 'cmd1' in req_arg or 'cmd2' in req_arg:
        if 'value1' in req_arg or 'value2' in req_arg:

            if req_arg.get('cmd1') == 'filter':
                if req_arg.get('value1'):
                    data_iter = filter_query(data_iter, req_arg.get('value1'))
                else:
                    return 'не задан value1'
            if req_arg.get('cmd2') == 'filter':
                if req_arg.get('value2'):
                    data_iter = filter_query(data_iter, req_arg.get('value2'))
                else:
                    return 'не задан value2'

            if req_arg.get('cmd1') == 'map':
                if req_arg.get('value1'):
                    try:
                        data_iter = filter_map(data_iter, req_arg.get('value1'))
                    except FilterMapColErrors as e:
                        return str(e)
                else:
                    return 'не задан value1'
            if req_arg.get('cmd2') == 'map':
                if req_arg.get('value2'):
                    try:
                        data_iter = filter_map(data_iter, req_arg.get('value2'))
                    except FilterMapColErrors as e:
                        return str(e)
                else:
                    return 'не задан value2'

            if req_arg.get('cmd1') == 'unique':
                if req_arg.get('value1') == '""':
                    data_iter = filter_unique(data_iter)
                else:
                    return 'value1 должен быть "" или не задан'
            if req_arg.get('cmd2') == 'unique':
                if req_arg.get('value2') == '""':
                    data_iter = filter_unique(data_iter)
                else:
                    return 'value2 должен быть "" или не задан'

            if req_arg.get('cmd1') == 'sort':
                if req_arg.get('value1') in ('asc', 'desc'):
                    if req_arg.get('value1') == 'asc':
                        data_iter = filter_sort(data_iter, False)
                    else:
                        data_iter = filter_sort(data_iter, True)
                else:
                    return 'не задан value1 или не задано значение ("asc", "desc")'
            if req_arg.get('cmd2') == 'sort':
                if req_arg.get('value2') in ('asc', 'desc'):
                    if req_arg.get('value2') == 'asc':
                        data_iter = filter_sort(data_iter, False)
                    else:
                        data_iter = filter_sort(data_iter, True)
                else:
                    return 'не задан value2 или не задано значение ("asc", "desc")'

            if req_arg.get('cmd1') == 'limit':
                if req_arg.get('value1') and req_arg.get('value1').isdigit():
                    data_iter = filter_limit(data_iter, int(req_arg.get('value1')))
                else:
                    return 'не задан value1 или введено не цифровое значение'
            if req_arg.get('cmd2') == 'limit':
                if req_arg.get('value2') and req_arg.get('value2').isdigit():
                    data_iter = filter_limit(data_iter, int(req_arg.get('value2')))
                else:
                    return 'не задан value2 или введено не цифровое значение'

        else:
            return 'не заданы value'

    return app.response_class(data_iter, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)
