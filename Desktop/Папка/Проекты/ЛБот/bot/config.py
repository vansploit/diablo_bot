import os
import vk_api

ver = "5.130"
vk_session = vk_api.VkApi(token=os.getenv('TOKEN'))
vk = vk_session.get_api()

def get_user_info(id_user):

	info = vk.users.get(user_ids = id_user, name_case = 'nom')

	return info[0]['first_name'], info[0]['last_name']
