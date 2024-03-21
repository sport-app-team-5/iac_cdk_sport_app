from aws_cdk import (aws_rds as rds, aws_ec2 as ec2, aws_logs as logs, aws_secretsmanager as secretsmanager,
                     Stack, RemovalPolicy, Duration)
from constructs import Construct


class Postgres(Stack):
    def __init__(self, scope: Construct, stack_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.vpc = vpc
        self.backup_retention_days: int = 7
        self.preferred_maintenance_window: str = "Sun:23:45-Mon:00:15"
        self.security_group_name: str = "database_security_group"
        self.secret_name: str = "database_secret"
        self.database_name: str = "sport_app"
        self.instance_name: str = "instance-postgres-sport-app"
        self.username: str = "sport_app"
        self.cloudwatch_logs_exports: list = ["postgresql"]
        self.security_group = self.create_security_group()
        self.secret = self.create_secret()
        self.create_database_instance()

    def create_security_group(self):
        security_group = ec2.SecurityGroup(self, self.security_group_name, vpc=self.vpc)
        security_group.add_ingress_rule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(5432))
        return security_group

    def create_secret(self):
        secret = secretsmanager.Secret(
            self, self.secret_name,
            secret_name=self.secret_name,
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username":"' + self.username + '"}',
                exclude_characters="\"@/\\ '",
                generate_string_key="password",
                password_length=30
            ),
            removal_policy=RemovalPolicy.DESTROY
        )
        return secret

    def create_database_instance(self):
        rds.DatabaseInstance(
            self,
            self.instance_name,
            instance_identifier=self.instance_name,
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_16),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_groups=[self.security_group],
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            storage_encrypted=False,
            database_name=self.database_name,
            credentials=rds.Credentials.from_secret(self.secret),
            backup_retention=Duration.days(self.backup_retention_days),
            preferred_maintenance_window=self.preferred_maintenance_window,
            cloudwatch_logs_exports=self.cloudwatch_logs_exports,
            cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH
        )
