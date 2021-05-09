import sys
import boto3
import logging 
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = boto3.client('cognito-idp')

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

def main():
    # create_cognito_user(
    #     'us-east-1_U8l3Pliwm',
    #     'admin'
    # )

if __name__ == '__main__':
    main()