import command_system
from config import get_user_info

def hello(msg_info):
   f_name, l_name = get_user_info(msg_info[3])
   message = f'Привет, {f_name}!'
   return message

hello_command = command_system.Command()

hello_command.keys = ['привет', 'hello', 'дратути', 'здравствуй', 'здравствуйте']
hello_command.description = 'Поприветствую тебя'
hello_command.need_parameter = True
hello_command.process = hello