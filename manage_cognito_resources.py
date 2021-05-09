import sys
import boto3
import logging 
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = boto3.client('cognito-idp')

def create_cognito_group(UserPoolId,Groupname):
    try:
        response = client.create_group(
            GroupName=Groupname,
            UserPoolId=UserPoolId,
            Description='{} - group'.format(Groupname)
        )
    except client.exceptions.GroupExistsException:
        logging.info('Group : {} Already Exists'.format(Groupname))
        return True
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info('Group : {} created'.format(Groupname))
        return True
    else:
        return False

def create_cognito_user(UserPoolId,Username,Email,TemporaryPassword):
    try:
        response = client.admin_create_user(
            UserPoolId=UserPoolId,
            Username=Username,
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
                {
                    'Name': 'email',
                    'Value': Email
                },
            ],
            ValidationData=[
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            TemporaryPassword=TemporaryPassword,
            ForceAliasCreation=False
        )
    except client.exceptions.UsernameExistsException:
        logging.info('User : {} with Email : {} Already Exists'.format(Username,Email))
        return False
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info('User : {} created with Email : {} '.format(Username,Email))
        return True
    else:
        return False
    
def delete_cognito_group(UserPoolId,Groupname):
    try:
        response = client.delete_group(
            GroupName=Groupname,
            UserPoolId=UserPoolId
        )
    except client.exceptions.ResourceNotFoundException:
        logging.info('Group : {} doesnt Exist'.format(Groupname))
        return True
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info('Group : {} deleted'.format(Groupname))
        return True
    else:
        return False

def delete_cognito_user(UserPoolId,Username):
    try:
        response = client.admin_disable_user(
            UserPoolId=UserPoolId,
            Username=Username
        )
    except client.exceptions.UserNotFoundException:
        logging.info('User : {} Not Dound'.format(Username))
        return True
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info('User : {} Disabled'.format(Username))
        response = client.admin_delete_user(
            UserPoolId=UserPoolId,
            Username=Username
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            logging.info('User : {} Deleted'.format(Username))
            return True
        else:
            return False
    else:
        return False

def get_cognito_users(UserPoolId):
    try:
        response=client.list_users(
            UserPoolId=UserPoolId
        )
    except client.exceptions.ResourceNotFoundException:
        logging.info('User not found in Pool : {}'.format(UserPoolId))
        return None
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        userlist = [ i['Username'] for i in response['Users']]
        logging.info('Users fetched from Pool : {}'.format(UserPoolId))
        return userlist
    else:
        return None

def get_cognito_groups(UserPoolId):
    try:
        response=client.list_groups(
            UserPoolId=UserPoolId
        )
    except client.exceptions.ResourceNotFoundException:
        logging.info('User not found in Pool : {}'.format(UserPoolId))
        return None
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        grouplist = [ i['GroupName'] for i in response['Groups']]
        logging.info('Groups fetched from Pool : {}'.format(UserPoolId))
        return grouplist
    else:
        return None

def add_user_to_group(UserPoolId,Username,GroupName):
    try:
        response = client.admin_add_user_to_group(
            UserPoolId=UserPoolId,
            Username=Username,
            GroupName=GroupName
        )
    except client.exceptions.ResourceNotFoundException:
        logging.info('Issue adding User {} to Group {}'.format(Username,GroupName))
        return False
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info('User {} added to group  {}'.format(Username,GroupName))
        return True
    else:
        return False

def remove_user_from_group(UserPoolId,Username,GroupName):
    try:
        response = client.admin_remove_user_from_group(
            UserPoolId=UserPoolId,
            Username=Username,
            GroupName=GroupName
        )
    except client.exceptions.ResourceNotFoundException:
        logging.info('User not found in Pool : {}'.format(UserPoolId))
        return False
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info('User {} Removed from group  {}'.format(Username,GroupName))
        return True
    else:
        return False


def get_cognito_groups_for_user(Username,UserPoolId):
    try:
        response = client.admin_list_groups_for_user(
            Username=Username,
            UserPoolId=UserPoolId
        )
    except client.exceptions.ResourceNotFoundException:
        logging.info('User not found in Pool : {}'.format(UserPoolId))
        return None
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        grouplist = [ i['GroupName'] for i in response['Groups']]
        logging.info('Groups fetched from Pool : {} for User: {}'.format(UserPoolId,Username))
        return grouplist
    else:
        return None