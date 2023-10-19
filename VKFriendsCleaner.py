import vk_api
token = 'token'
api = vk_api.VkApi(token=token).get_api()
for friend in api.friends.getMutual(target_uids=','.join([str(uid) for uid in api.friends.get()['items']])):
    if friend['common_count'] == 0:
        friend_name = api.users.get(user_ids=friend['id'])[0]
        api.friends.delete(user_id=friend['id'])
        print('Удалил друга '+friend_name['first_name']+' '+friend_name['last_name'])
