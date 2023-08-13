from quopri import decodestring
from framework.my_request import GetRequests, PostRequests
from patterns.creational_patterns import Logger

logger = Logger('main')

class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            msg_dict = Framework.decode_value(data)
            request['data'] = msg_dict
            logger.log(logger, f'Нам пришёл post-запрос: {Framework.decode_value(data)}')

        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            if Framework.decode_value(request_params):
                logger.log(logger, f'Нам пришли GET-параметры: {Framework.decode_value(request_params)}')

            # находим нужный контроллер
            # отработка паттерна page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

            # наполняем словарь request элементами
            # этот словарь получат все контроллеры
            # отработка паттерна front controller
        for front in self.fronts:
            front(request)
            # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
