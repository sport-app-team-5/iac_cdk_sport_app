import aws_cdk.assertions as assertions
from sport_app_iac_aws_cdk import VirtualPrivateCloud, DockerHubCredentials
from sport_app_iac_aws_cdk.backend.user.ecr import UserEcr


class TestCommonAwsSdkStack:
    def test_vpc_created(self, app, env):
        stack = VirtualPrivateCloud(app, "VirtualPrivateCloud", env=env)
        assertions.Template.from_stack(stack)

    def test_docker_hub_secret(self, app, env):
        stack = DockerHubCredentials(app, "DockerHubCredentials", env=env)
        assertions.Template.from_stack(stack)

    def test_ecr(self, app, env):
        stack = UserEcr(app, "UserEcr", env=env)
        assertions.Template.from_stack(stack)
