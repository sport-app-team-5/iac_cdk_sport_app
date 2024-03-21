import aws_cdk.assertions as assertions
from sport_app_iac_aws_cdk import Vpc
from sport_app_iac_aws_cdk.frontend.ecr import SportAppEcr
from sport_app_iac_aws_cdk.frontend.frontend import SportAppFrontend
from sport_app_iac_aws_cdk.frontend.pipeline import SportAppFrontendEcrPipeline
from sport_app_iac_aws_cdk.frontend.secret import SportAppFrontendSecret


class TestFrontendAwsSdkStack:
    def test_sport_app_frontend_ecr_pipeline(self, app, docker_hub_secret_mock):
        stack = SportAppFrontendEcrPipeline(app, "SportAppFrontendEcrPipeline", docker_hub_secret_mock)
        assertions.Template.from_stack(stack)

    def test_sport_app_frontend_deploy(self, app, env, docker_hub_secret_mock):
        vpc_stack = Vpc(app, "Vpc", env=env)
        pipe_front = SportAppFrontendEcrPipeline(app, "SportAppFrontendEcrPipeline", docker_hub_secret_mock,
                                                env=env)
        secret_front = SportAppFrontendSecret(app, "SportAppFrontendSecret", env=env)
        stack = SportAppFrontend(app, "SportAppFrontend", vpc_stack.vpc, pipe_front.pipeline,
                                 secret_front.secret, env=env)
        assertions.Template.from_stack(stack)

    def test_sport_app_ecr(self, app, env):
        stack = SportAppEcr(app, "SportAppEcr", env=env)
        assertions.Template.from_stack(stack)
