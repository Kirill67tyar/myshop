def get_view_at_console2(obj, delimiter='*', unpack=False, sep='\n'):
    """

    :param obj: объект который нужно вывести в консоль
    :param delimiter: то каким символом разделять вывод в консоли сверху и снизу
    :param unpack: распаковывать эдемент на методы и атрибуты или нет (помещать в dir())
    :param sep: по умолчанию равен '\n'
    :return:
    """
    unpack_obj = None
    name = None
    if hasattr(obj, '__name__'):
        name = obj.__name__
    name = name + ' :' if name else ''
    if unpack:
        unpack_obj = dir(obj)
    if delimiter:
        delimiter = delimiter * 25

        if unpack_obj:
            return print(sep, delimiter, name, *unpack_obj, delimiter, sep ,sep='\n')
        else:
            return print(sep, delimiter, name, obj, delimiter, sep, sep='\n')
    else:
        if unpack_obj:
            return print(sep, name, *unpack_obj, sep ,sep='\n')
        else:
            return print(sep, name, obj, sep, sep='\n')





def get_view_at_console(obj, delimiter='*', unpack=False, sep='\n'):
    """

    :param obj: объект который нужно вывести в консоль
    :param delimiter: то каким символом разделять вывод в консоли сверху и снизу
    :param unpack: распаковывать эдемент на методы и атрибуты или нет (помещать в dir())
    :param sep: по умолчанию равен '\n'
    :return:
    """

    name = getattr(obj, '__name__') + ' :' if hasattr(obj, '__name__') else ''
    if unpack:
        args = [sep, name, *dir(obj), sep]
    else:
        args = [sep, name, obj, sep]
    if delimiter:
        delimiter = delimiter * 25
        args.insert(1, delimiter)
        args.insert(-1, delimiter)
    return print(*args, sep='\n')
