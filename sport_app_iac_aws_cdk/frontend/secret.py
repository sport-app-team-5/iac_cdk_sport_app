from aws_cdk import Stack, aws_secretsmanager as secretsmanager
from constructs import Construct


class SportAppFrontendSecret(Stack):

    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)

        self.secret_name: str = 'sport_app_frontend'
        self.secret = self.create_secret()

    def create_secret(self):
        secret = secretsmanager.Secret(self, self.secret_name, secret_name=self.secret_name)
        return secret
