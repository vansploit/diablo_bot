import os
import importlib
from command_system import command_list

def load_modules():

    # путь от рабочей директории, ее можно изменить в настройках приложения
    files = os.listdir("commands")

    modules = filter(lambda x: x.endswith('.py'), files)

    for m in modules:
        importlib.import_module("commands." + m[0:-3])


def create_answer(msg_info):

    load_modules()

    for c in command_list:

        if msg_info[2].lower() in c.keys:

            if c.need_parameter == True:

                message = c.process(msg_info)

            else:

                message = c.process()

        else:

                message = None

    if message is not None:

        return message

    else:

        result = 'Error'

    return result