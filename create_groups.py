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

def main():
    # create_cognito_group(
    #     'us-east-1_U8l3Pliwm',
    #     'admin'
    # )

if __name__ == '__main__':
    main()