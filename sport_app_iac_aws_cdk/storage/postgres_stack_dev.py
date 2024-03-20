from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_secretsmanager as secretsmanager,
    Stack,
    RemovalPolicy,
    Duration
)
from constructs import Construct


class Postgres(Stack):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create config
        backup_retention_days: int = 7
        preferred_maintenance_window: str = "Sun:23:45-Mon:00:15"
        security_group_name: str = "database_security_group"
        secret_name: str = "database_secret"
        database_name: str = "sport_app"
        instance_name: str = "instance_postgres_sport_app"
        username: str = "sport_app"
        cloudwatch_logs_exports: list = ["postgresql"]

        # Create security group
        security_group = ec2.SecurityGroup(self, security_group_name, vpc=vpc)

        # Only in dev storage
        security_group.add_ingress_rule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(5432))

        # Create secret
        secret = secretsmanager.Secret(
            self, secret_name,
            secret_name=secret_name,
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username":"' + username + '"}',
                exclude_characters="\"@/\\ '",
                generate_string_key="password",
                password_length=30
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        rds.DatabaseInstance(
            self,
            instance_name,
            instance_identifier=instance_name,
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_12),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_groups=[security_group],
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=True,
            storage_encrypted=True,
            database_name=database_name,
            credentials=rds.Credentials.from_secret(secret),
            backup_retention=Duration.days(backup_retention_days),
            preferred_maintenance_window=preferred_maintenance_window,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH
        )
