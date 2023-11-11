import boto3
import json
from ..utils.constants import POOL_ID, CLIENT_ID, API_ENDPOINT

from jose import jwt
import requests
import botocore.exceptions

EMAIL_ADDR = "mauriciohvvilla1@gmail.com"


def callApi(token):
        headers = {'Authorization': token}
        # body = {'FakeData': 'MYFAKEDATA123456'}
        body = {
                "FakeData": "MYFAKEDATA123456",
                "MoreFakes": "MOREFAKEDATA123123"
                }
        url = API_ENDPOINT
        r = requests.post(url, headers=headers, json=body)
        print(f"\nAPI POST\n{r.status_code}\n{r.text}")

#TODO add getting username, email, and password with argparse
#TODO store given username and password to a file, to readback from later
class Authentication():
    def signup(self):
            cidp = boto3.client('cognito-idp', region_name="us-east-2")

            try:
                    r = cidp.sign_up(
                            ClientId=CLIENT_ID,
                            Username='cognito-py-demo',
                            Password='D0lphins!',
                            UserAttributes=[{'Name': 'email',
                                            'Value': EMAIL_ADDR}])
                    print(json.dumps(r, indent=2))

            except botocore.exceptions.ClientError as error:
                    print(f"Error during signup:\n{error}")

    # decoding tokens with jose (JavaScript Object Signing and Encryption) and checking the signature
    #  of some of the claims at the same time.
    def decodeToken(self, token):
            jwks_url = 'https://cognito-idp.{}.amazonaws.com/{}/' \
                            '.well-known/jwks.json'.format(
                                    'us-east-2',
                                    POOL_ID)
            
            jwks = requests.get(jwks_url).json()

            decoded = jwt.decode(token, jwks)
            print("Decoded Token:")
            print(json.dumps(decoded, indent=2))
            return decoded

    # standard flow is USER_SRP_AUTH. password is never sent over wire.
    # python SDK doesnt have methods built in to easily deal with SRP
    # using USER_PASSWORD_AUTH flow is much less secure, but easier to use in python
    def authenticate(self):
            cidp = boto3.client('cognito-idp', region_name="us-east-2")
            r = cidp.initiate_auth(
                    AuthFlow='USER_PASSWORD_AUTH',
                    AuthParameters={
                            'USERNAME': 'cognito-py-demo',
                            'PASSWORD': 'D0lphins!'
                    },
                    ClientId=CLIENT_ID
            )
            print(json.dumps(r, indent=2))
            # print(f"access token:\n{r['AuthenticationResult']['AccessToken']}")
            access_token = r['AuthenticationResult']['AccessToken']
            # token = decodeToken(access_token)
            id_token = r['AuthenticationResult']['IdToken']
            callApi(id_token)