import sys
import boto3
import logging 
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = boto3.client('cognito-idp')


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

def main():
    # create_cognito_user(
    #     'us-east-1_U8l3Pliwm',
    #     'ashwinkumarnaik91',
    #     'ashwinkumarnaik91@gmail.com',
    #     'TestP@ssw0rd@321'
    # )

if __name__ == '__main__':
    main()