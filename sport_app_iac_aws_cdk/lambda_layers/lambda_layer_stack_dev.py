from aws_cdk import Stack, aws_lambda, RemovalPolicy
from constructs import Construct


class LambdaLayers(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.boto3_lambda_layer = self.create_boto3_lambda_layer()
        self.sqlalchemy_psycopg2_lambda_layer = self.create_sqlalchemy_psycopg2_lambda_layer()
        self.dotenv_lambda_layer = self.create_dotenv_lambda_layer()
        self.requests_layer = self.create_requests_layer()

    def create_sqlalchemy_psycopg2_lambda_layer(self):
        sqlalchemy_psycopg2_lambda_layers = aws_lambda.LayerVersion(
            self,
            "sqlalchemy-psycopg2-lambda-layer",
            layer_version_name="sqlalchemy-psycopg2-lambda-layer",
            code=aws_lambda.Code.from_asset("lambda-layers/sqlalchemy-psycopg2/modules"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            description="Lambda Layer for Python with sqlalchemy and psycopg2 library",
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            removal_policy=RemovalPolicy.DESTROY
        )
        return sqlalchemy_psycopg2_lambda_layers

    def create_dotenv_lambda_layer(self):
        dotenv_lambda_layers = aws_lambda.LayerVersion(
            self,
            "dotenv-lambda-layer",
            layer_version_name="dotenv-lambda-layer",
            code=aws_lambda.Code.from_asset("lambda-layers/dotenv/modules"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            description="Lambda Layer for Python with dotenv library",
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            removal_policy=RemovalPolicy.DESTROY
        )
        return dotenv_lambda_layers

    def create_boto3_lambda_layer(self):
        boto3_lambda_layers = aws_lambda.LayerVersion(
            self,
            "boto3-lambda-layer",
            layer_version_name="boto3-lambda-layer",
            code=aws_lambda.Code.from_asset("lambda-layers/boto3/modules"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            description="Lambda Layer for Python with boto3 library",
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            removal_policy=RemovalPolicy.DESTROY
        )
        return boto3_lambda_layers

    def create_requests_layer(self):
        pycryptodome_layer = aws_lambda.LayerVersion(
            self,
            "requests-lambda-layer",
            layer_version_name="requests-lambda-layer",
            code=aws_lambda.Code.from_asset("lambda-layers/requests/modules"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            description="Lambda Layer for Python with requests library",
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            removal_policy=RemovalPolicy.DESTROY
        )
        return pycryptodome_layer
