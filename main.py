import os
import sys
import utils
import manage_cognito_resources
import logging 
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def main():
    USER_POOL_ID = os.getenv('USER_POOL_ID')
    if USER_POOL_ID is None:
        print('Export the Env Var USER_POOL_ID .')
        sys.exit()
    USER_MAP_FILE = os.getenv('USER_MAP_FILE','usermap.properties')
    group_map=utils.parse_users_groups(USER_MAP_FILE)
    
    groups = list(group_map.keys())
    usermap = { list(j.keys())[0]:list(j.values())[0] for i in groups for j in group_map[i] }
    user_group_map = {}
    for user in usermap.keys():
        user_group_map[user] = []
        for group in group_map:
            userlist = [ list(i.keys())[0] for i in group_map[group]]
            if user in userlist:
                user_group_map[user].append(group)
    
    cognito_users = manage_cognito_resources.get_cognito_users(USER_POOL_ID)
    cognito_groups = manage_cognito_resources.get_cognito_groups(USER_POOL_ID)
    cognito_user_group_map = {}
    for c_user in cognito_users:
        cognito_user_group_map[c_user] = manage_cognito_resources.get_cognito_groups_for_user(c_user,USER_POOL_ID)

    if not utils.compare_list(groups,cognito_groups):
        if len(groups) > len(cognito_groups):
            for each_group in utils.diff_list(groups,cognito_groups):
                manage_cognito_resources.create_cognito_group(USER_POOL_ID,each_group)
        else:
            for each_group in utils.diff_list(cognito_groups,groups):
                manage_cognito_resources.delete_cognito_group(USER_POOL_ID,each_group)
    else:
        logging.info('No Change in Groups')
    
    config_source = True
    if not utils.compare_list(list(usermap.keys()),cognito_users):
        if len(list(usermap.keys())) > len(cognito_users):
            for each_user,each_email in usermap.items():
                manage_cognito_resources.create_cognito_user(USER_POOL_ID,each_user,each_email,utils.generate_random_password())
                cognito_user_group_map[each_user] = manage_cognito_resources.get_cognito_groups_for_user(each_user,USER_POOL_ID)
        else:
            config_source = True
            for each_user in utils.diff_list(cognito_users,list(usermap.keys())):
                manage_cognito_resources.delete_cognito_user(USER_POOL_ID,each_user)
    else:
        logging.info('No Change in Users')

    for user in usermap.keys() if config_source else cognito_users:
        if not utils.compare_list(user_group_map[user],cognito_user_group_map[user]):
            if len(user_group_map[user]) > len(cognito_user_group_map[user]):
                for group in user_group_map[user]:
                    manage_cognito_resources.add_user_to_group(USER_POOL_ID,user,group)
            else:
                for group in utils.diff_list(cognito_user_group_map[user],user_group_map[user]):
                    manage_cognito_resources.remove_user_from_group(USER_POOL_ID,user,group)
        else:
            logging.info('No Change in User to Group Mapping for user: {}'.format(user))

if __name__ == '__main__':
    main()