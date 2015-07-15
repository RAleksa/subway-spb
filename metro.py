# -*- coding: utf-8 -*-

import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

stations = {0: u'Девяткино', 
            1: u'Гражданский проспект',
            2: u'Академическая',
            3: u'Политехническая',
            4: u'Площадь Мужества',
            5: u'Лесная',
            6: u'Выборгская',
            7: u'Площадь Ленина',
            8: u'Чернышевская',
            9: u'Площадь Восстания',
            10: u'Владимирская',
            11: u'Пушкинская',
            12: u'Технологический институт-1',
            13: u'Балтийская',
            14: u'Нарвская',
            15: u'Кировский завод',
            16: u'Автово',
            17: u'Ленинский проспект',
            18: u'Проспект Ветеранов',
            19: u'Парнас',
            20: u'Проспект Просвещения',
            21: u'Озерки',
            22: u'Удельная',
            23: u'Пионерская',
            24: u'Чёрная речка',
            25: u'Петроградская',
            26: u'Горьковская',
            27: u'Невский проспект',
            28: u'Сенная площадь',
            29: u'Технологический институт-2',
            30: u'Фрунзенская',
            31: u'Московские ворота',
            32: u'Электросила',
            33: u'Парк Победы',
            34: u'Московская',
            35: u'Звёздная',
            36: u'Купчино',
            37: u'Приморская',
            38: u'Василеостровская',
            39: u'Гостиный двор',
            40: u'Маяковская',
            41: u'Площадь Александра Невского-1',
            42: u'Елизаровская',
            43: u'Ломоносовская',
            44: u'Пролетарская',
            45: u'Обухово',
            46: u'Рыбацкое',
            47: u'Спасская',
            48: u'Достоевская',
            49: u'Лиговский проспект',
            50: u'Площадь Александра Невского-2',
            51: u'Новочеркасская',
            52: u'Ладожская',
            53: u'Проспект Большевиков',
            54: u'Улица Дыбенко',
            55: u'Комендантский проспект',
            56: u'Старая Деревня',
            57: u'Крестовский остров',
            58: u'Чкаловская',
            59: u'Спортивная',
            60: u'Адмиралтейская',
            61: u'Садовая',
            62: u'Звенигородская',
            63: u'Обводный канал',
            64: u'Волковская',
            65: u'Бухарестская',
            66: u'Международная'
            }

g = {0: {1: 3},
     1: {0: 3, 2: 3},
     2: {1: 3, 3: 2},
     3: {2: 2, 4: 3},
     4: {3: 3, 5: 3},
     5: {4: 3, 6: 3},
     6: {5: 3, 7: 2},
     7: {6: 2, 8: 3},
     8: {7: 3, 9: 2},
     9: {8: 2, 40: 2, 10: 2},
     10: {9: 2, 11: 2, 48: 2},
     11: {10: 2, 12: 2, 62: 2},
     12: {11: 2, 13: 2, 29: 1},
     13: {12: 2, 14: 3},
     14: {13: 3, 15: 4},
     15: {14: 4, 16: 2},
     16: {15: 2, 17: 3},
     17: {16: 3, 18: 2},
     18: {17: 2},
     19: {20: 3},
     20: {19: 3, 21: 2},
     21: {20: 2, 22: 3},
     22: {21: 3, 23: 3},
     23: {22: 3, 24: 3},
     24: {23: 3, 25: 4},
     25: {24: 4, 26: 2},
     26: {25: 2, 27: 4},
     27: {26: 4, 28: 2, 39: 2},
     28: {27: 2, 29: 3, 47: 3, 61: 3},
     29: {28: 3, 30: 2, 12: 1},
     30: {29: 2, 31: 2},
     31: {30: 2, 32: 2},
     32: {31: 2, 33: 2},
     33: {32: 2, 34: 3},
     34: {33: 3, 35: 4},
     35: {34: 4, 36: 3},
     36: {35: 3},
     37: {38: 4},
     38: {37: 4, 39: 4},
     39: {38: 4, 40: 3, 27: 2},
     40: {39: 3, 41: 3, 9: 2},
     41: {40: 3, 42: 5, 50: 2},
     42: {41: 5, 43: 3},
     43: {42: 3, 44: 3},
     44: {43: 3, 45: 3},
     45: {44: 3, 46: 4},
     46: {45: 4},
     47: {48: 4, 28: 3, 61: 3},
     48: {47: 4, 49: 2, 10: 2},
     49: {48: 2, 50: 2},
     50: {49: 2, 51: 3, 41: 2},
     51: {50: 3, 52: 3},
     52: {51: 3, 53: 3},
     53: {52: 3, 54: 2},
     54: {53: 2},
     55: {56: 3},
     56: {55: 3, 57: 3},
     57: {56: 3, 58: 4},
     58: {57: 4, 59: 2},
     59: {58: 2, 60: 3},
     60: {59: 3, 61: 3},
     61: {60: 3, 62: 4, 47: 3, 28: 3},
     62: {61: 4, 63: 3, 11: 2},
     63: {62: 3, 64: 3},
     64: {63: 3, 65: 3},
     65: {64: 3, 66: 3},
     66: {65: 3}
     }

n = 67

stations_rev_lower = {}
for i in range(n):
    stations_rev_lower[stations[i].lower()] = i

stations_alph = []
for i in range(n):
    stations_alph.append(stations[i])
stations_alph.sort()

def color(v):
    if v <= 18:
        return '#BC021E' # красная
    else:
        if v <= 36:
            return '#0E7EA3' # синяя
        else:
            if v <= 46:
                return '#088B1C' # зеленая
            else:
                if v <= 54:
                    return '#C28C04' # желтая
                else:
                    return '#9C1995' # фиолетовая

def norm_path(path):
    ans = []
    transfer = 0
    for i in range(len(path)):
        if i != 0 and color(path[i]) != color(path[i - 1]):
            transfer += 1
        ans.append((stations[path[i]], color(path[i])))
    return ans, transfer

def dijkstra(s, r):
    if s == r:
        return 0, []
    
    d = [float('inf')] * n
    p = [-1] * n
    d[s] = 0
    u = [False] * n
    
    for i in range(n):
        v = -1
        for j in range(n):
            if (not u[j]) and (v == -1 or d[j] < d[v]):
                v = j
        if d[v] == float('inf'):
            break
        u[v] = True
        if v == r:
            path = []
            while r != s:
                path.append(r)
                r = p[r]
            path.append(s)
            path = list(reversed(path))
            return d[v], path
        
        for j in range(len(g[v])):
            to = g[v].items()[j][0]
            length = g[v].items()[j][1]
            if d[v] + length < d[to]:
                d[to] = d[v] + length
                p[to] = v

def transfer_text(transfer):
    if transfer == 0:
        return u'Без пересадок'
    if transfer == 1:
        return u'1 пересадка'
    return str(transfer) + u' пересадки'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'stations': stations_alph,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        begin = self.request.get('begin').strip().lower()
        end = self.request.get('end').strip().lower()
        try:
            u = stations_rev_lower[begin]
            v = stations_rev_lower[end]
            path = []
            res, path = dijkstra(u, v)
            path, transfer = norm_path(path)
            transfer = transfer_text(transfer)

            template_values = {
                'result': res,
                'stations': stations_alph,
                'st_begin': stations[u],
                'st_end': stations[v],
                'path': path,
                'transfer': transfer,
                'check': False,
            }
        except:
            template_values = {
                'stations': stations_alph,
                'check': True,
                # 'error': begin + ' - ' + end,
            }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)