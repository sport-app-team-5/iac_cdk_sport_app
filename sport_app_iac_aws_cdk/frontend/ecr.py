from aws_cdk import Stack, aws_ecr as ecr, CfnOutput
from constructs import Construct


class SportAppEcr(Stack):
    def __init__(self, scope: Construct, stack_id: str, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.ecr_repository_name: str = 'sport_app_frontend_ecr'
        self.ecr_repository_name_cfn_output: str = 'SportAppFrontendEcrCfnOutput'
        self.create_ecr()

    def create_ecr(self):
        ecr_repository = ecr.Repository(self, self.ecr_repository_name, repository_name=self.ecr_repository_name)
        CfnOutput(self, self.ecr_repository_name_cfn_output, value=ecr_repository.repository_name,
                  export_name=self.ecr_repository_name_cfn_output)
