import sys
import boto3
import logging 
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = boto3.client('cognito-idp')

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

def main():
    delete_cognito_user(
        'us-east-1_U8l3Pliwm',
        'ashwinkumarnaik91'
    )

if __name__ == '__main__':
    main()