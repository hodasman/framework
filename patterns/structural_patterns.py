from time import time

from patterns.creational_patterns import Logger

logger = Logger('main')


# структурный паттерн - Декоратор
class AppRoute:
    routes = {}

    def __init__(self, url):
        '''
        Сохраняем значение переданного параметра
        '''

        self.url = url

    def __call__(self, cls):
        '''
        Сам декоратор
        '''
        AppRoute.routes[self.url] = cls()


# структурный паттерн - Декоратор
class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        '''
        сам декоратор
        '''

        # это вспомогательная функция будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            '''
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            '''

            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                logger.log(logger, f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
