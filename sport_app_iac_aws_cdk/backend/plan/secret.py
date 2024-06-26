from aws_cdk import Stack, aws_secretsmanager as secretsmanager
from constructs import Construct


class PlanBackendSecret(Stack):

    def __init__(self, scope: Construct, stack_id: str, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.secret_name: str = 'plan_backend'
        self.secret = self.create_secret()

    def create_secret(self):
        secret = secretsmanager.Secret(self, self.secret_name, secret_name=self.secret_name)
        return secret
