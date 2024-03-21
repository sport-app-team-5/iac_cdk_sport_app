import aws_cdk.assertions as assertions
from sport_app_iac_aws_cdk import Vpc
from sport_app_iac_aws_cdk.storage import Postgres


class TestPostgresAwsSdkStack:
    def test_postgres_created(self, app, env):
        vpc_stack = Vpc(app, "Vpc", env=env)
        stack = Postgres(app, "Postgres", vpc_stack.vpc, env=env)
        assertions.Template.from_stack(stack)
