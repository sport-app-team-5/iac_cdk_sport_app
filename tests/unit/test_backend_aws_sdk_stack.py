import aws_cdk.assertions as assertions
from sport_app_iac_aws_cdk import Vpc
from sport_app_iac_aws_cdk.backend.plan import PlanBackendEcrPipeline, PlanBackendSecret, PlanBackend, PlanEcr
from sport_app_iac_aws_cdk.backend.service import AdditionalServiceBackend, AdditionalServiceBackendSecret, \
    AdditionalServiceBackendEcrPipeline, AdditionalServiceEcr
from sport_app_iac_aws_cdk.backend.user import UserBackendEcrPipeline, UserBackendSecret, UserBackend, UserEcr


class TestBackendUserAwsSdkStack:
    def test_user_backend_ecr_pipeline(self, app, docker_hub_secret_mock):
        stack = UserBackendEcrPipeline(app, "UserBackendEcrPipeline", docker_hub_secret_mock)
        assertions.Template.from_stack(stack)

    def test_user_backend_deploy(self, app, env, docker_hub_secret_mock):
        vpc_stack = Vpc(app, "Vpc", env=env)
        pipe_back = UserBackendEcrPipeline(app, "UserBackendEcrPipeline", docker_hub_secret_mock,
                                           env=env)
        secret_back = UserBackendSecret(app, "UserBackendSecret", env=env)
        stack = UserBackend(app, "UserBackend", vpc_stack.vpc, pipe_back.pipeline,
                            secret_back.secret, env=env)
        assertions.Template.from_stack(stack)

    def test_user_ecr(self, app, env):
        stack = UserEcr(app, "UserEcr", env=env)
        assertions.Template.from_stack(stack)


class TestBackendPlanAwsSdkStack:
    def test_plan_backend_ecr_pipeline(self, app, docker_hub_secret_mock):
        stack = PlanBackendEcrPipeline(app, "PlanBackendEcrPipeline", docker_hub_secret_mock)
        assertions.Template.from_stack(stack)

    def test_plan_backend_deploy(self, app, env, docker_hub_secret_mock):
        vpc_stack = Vpc(app, "Vpc", env=env)
        pipe_back = PlanBackendEcrPipeline(app, "PlanBackendEcrPipeline", docker_hub_secret_mock,
                                           env=env)
        secret_back = PlanBackendSecret(app, "PlanBackendSecret", env=env)
        stack = PlanBackend(app, "PlanBackend", vpc_stack.vpc, pipe_back.pipeline,
                            secret_back.secret, env=env)
        assertions.Template.from_stack(stack)

    def test_plan_ecr(self, app, env):
        stack = PlanEcr(app, "PlanEcr", env=env)
        assertions.Template.from_stack(stack)


class TestBackendAdditionalServiceAwsSdkStack:
    def test_additional_service_backend_ecr_pipeline(self, app, docker_hub_secret_mock):
        stack = AdditionalServiceBackendEcrPipeline(app, "AdditionalServiceBackendEcrPipeline", docker_hub_secret_mock)
        assertions.Template.from_stack(stack)

    def test_additional_service_backend_deploy(self, app, env, docker_hub_secret_mock):
        vpc_stack = Vpc(app, "Vpc", env=env)
        pipe_back = AdditionalServiceBackendEcrPipeline(app, "AdditionalServiceBackendEcrPipeline",
                                                        docker_hub_secret_mock,
                                                        env=env)
        secret_back = AdditionalServiceBackendSecret(app, "AdditionalServiceBackendSecret", env=env)
        stack = AdditionalServiceBackend(app, "AdditionalServiceBackend", vpc_stack.vpc, pipe_back.pipeline,
                                         secret_back.secret, env=env)
        assertions.Template.from_stack(stack)

    def test_additional_service_ecr(self, app, env):
        stack = AdditionalServiceEcr(app, "AdditionalServiceEcr", env=env)
        assertions.Template.from_stack(stack)
