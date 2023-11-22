from string import ascii_letters


class PlanetNameError(Exception):
    pass


planets = {'Марс': 'Mars', 'Меркурий': 'Mercury', 'Венера': 'Venus',
           'Юпитер': 'Jupiter', 'Сатурн': 'Saturn',
           'Уран': 'Uranus', 'Нептун': 'Neptune', 'Плутон': 'Pluto'}


def valid_planet_name(text):
    '''Проверка на корректность планеты, перевод с русского на английский'''

    input_lst = text.split()
    if len(input_lst) != 2:
        raise PlanetNameError(
            'Как-то некорректно сформулирован запрос. То ли планеты такой нет, то ли с синтаксисом кто-то напутал... '
            'Попробуй еще раз, шаблон следующий: /planet планета')
    input_planet = input_lst[-1].lower().capitalize()
    en_planet = all(map(lambda c: c in ascii_letters, input_planet))
    if en_planet and input_planet in planets.values():
        return input_planet
    elif not en_planet and input_planet in planets.keys():
        return planets.get(input_planet)
    else:
        raise PlanetNameError(
            'Как-то некорректно сформулирован запрос. То ли планеты такой нет, то ли с синтаксисом кто-то напутал... '
            'Попробуй еще раз, шаблон следующий: /planet планета')


if __name__ == '__main__':
    try:
        text = '/planet маравс'
        print(valid_planet_name(text))
    except PlanetNameError as err:
        print(err)
