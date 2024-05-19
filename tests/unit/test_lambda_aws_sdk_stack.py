from aws_cdk import assertions
from sport_app_iac_aws_cdk.lambda_layers import LambdaLayers


class TestLambdaLayersSdkStack:
    def test_lambda_layer_created(self, app, env):
        stack = LambdaLayers(app, "LambdaLayers", env=env)
        assertions.Template.from_stack(stack)
