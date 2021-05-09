import sys
import boto3
import logging 
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = boto3.client('cognito-idp')


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

def main():
    # create_cognito_user(
    #     'us-east-1_U8l3Pliwm',
    #     'ashwinkumarnaik91',
    #     'ashwinkumarnaik91@gmail.com',
    #     'TestP@ssw0rd@321'
    # )

if __name__ == '__main__':
    main()