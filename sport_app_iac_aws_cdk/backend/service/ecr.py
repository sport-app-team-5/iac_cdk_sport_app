from aws_cdk import Stack, aws_ecr as ecr, CfnOutput
from constructs import Construct


class AdditionalServiceEcr(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)

        self.ecr_repository_name: str = 'additional_service_backend_ecr'
        self.create_ecr()

    def create_ecr(self):
        ecr_repository = ecr.Repository(self, self.ecr_repository_name, repository_name=self.ecr_repository_name)
        CfnOutput(self, 'AdditionalServiceBackendEcrName', value=ecr_repository.repository_name,
                  export_name="AdditionalServiceBackendEcrName")
