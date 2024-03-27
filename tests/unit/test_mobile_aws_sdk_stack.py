import aws_cdk.assertions as assertions
from sport_app_iac_aws_cdk.mobile.pipeline import SportAppMobileEcrPipeline


class TestMobileAwsSdkStack:
    def test_sport_app_frontend_ecr_pipeline(self, app, docker_hub_secret_mock):
        stack = SportAppMobileEcrPipeline(app, "SportAppMobileEcrPipeline", docker_hub_secret_mock)
        assertions.Template.from_stack(stack)
