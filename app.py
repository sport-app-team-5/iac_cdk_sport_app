import aws_cdk as cdk
from aws_cdk import Environment
from sport_app_iac_aws_cdk import DockerHubCredentials, VirtualPrivateCloud
from sport_app_iac_aws_cdk.backend.plan import PlanBackendSecret, PlanEcr, PlanBackendEcrPipeline, PlanBackend
from sport_app_iac_aws_cdk.backend.user import UserBackendSecret, UserBackend, UserBackendEcrPipeline
from sport_app_iac_aws_cdk.backend.user.ecr import UserEcr

app = cdk.App()
aws_account = app.node.try_get_context("aws_account")
aws_region = app.node.try_get_context("aws_region")
env = Environment(account=aws_account, region=aws_region)

# Common
vpc = VirtualPrivateCloud(app, "VirtualPrivateCloud", env=env)
docker_hub_secret = DockerHubCredentials(app, "DockerHubCredentials", env=env)

# Backend user
user_backend_secret = UserBackendSecret(app, "UserBackendSecret", env=env)
user_ecr_repository = UserEcr(app, "UserEcr", env=env)
user_backend_ecr_pipeline = UserBackendEcrPipeline(app, "UserBackendEcrPipeline", docker_hub_secret.secret, env=env)
user_backend = UserBackend(app, "UserBackend", vpc.vpc, user_backend_ecr_pipeline.pipeline,
                           user_backend_secret.secret, env=env)

# Backend plan
plan_backend_secret = PlanBackendSecret(app, "PlanBackendSecret", env=env)
plan_ecr_repository = PlanEcr(app, "PlanEcr", env=env)
plan_backend_ecr_pipeline = PlanBackendEcrPipeline(app, "PlanBackendEcrPipeline", docker_hub_secret.secret, env=env)
plan_backend = PlanBackend(app, "PlanBackend", vpc.vpc, plan_backend_ecr_pipeline.pipeline,
                           plan_backend_secret.secret, env=env)

app.synth()
