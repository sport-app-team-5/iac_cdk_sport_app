from aws_cdk import (Stack, aws_ecr as ecr, aws_elasticloadbalancingv2 as elastic_load_balancer,
                     aws_ecs as ecs, aws_codepipeline_actions as codepipeline_actions, aws_codepipeline as codepipeline,
                     aws_iam as iam, aws_logs as logs, Fn)
from constructs import Construct


class SportAppFrontend(Stack):

    def __init__(self, scope: Construct, _id: str, vpc, pipeline, secret, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)

        self.vpc = vpc
        self.pipeline = pipeline
        self.secret = secret
        self.fargate_cluster_name = 'sport_app_cluster'
        self.load_balancer_name = 'sport_app_lb'
        self.load_balancer_listener_name = 'sport_app_listener'
        self.fargate_task_name = 'sport_app_task'
        self.fargate_container_name = 'sport_app_container'
        self.fargate_service_name = 'sport_app_service'
        ecr_repository_name = Fn.import_value('sport_app_frontend_ecr')
        self.ecr_repository = ecr.Repository.from_repository_name(self, ecr_repository_name, ecr_repository_name)

        self.cluster = self.create_fargate_cluster()
        self.load_balancer = self.create_load_balance()
        self.listener = self.create_listener()
        self.task_definition = self.create_fargate_task_definition()
        self.add_fargate_container_to_task()
        self.ecs_service = self.add_service_to_cluster()
        self.log_policy = self.create_log_policy_observability()
        self.add_roles_to_task()
        self.add_listener_to_load_balancer()
        self.add_stage_to_pipeline()
        self.grant_permissions_to_task()

    def create_fargate_cluster(self):
        cluster = ecs.Cluster(self, self.fargate_cluster_name, vpc=self.vpc)
        return cluster

    def create_load_balance(self):
        load_balancer = elastic_load_balancer.ApplicationLoadBalancer(self, self.load_balancer_name, vpc=self.vpc,
                                                                      internet_facing=True)
        return load_balancer

    def create_listener(self):
        listener = self.load_balancer.add_listener(self.load_balancer_listener_name, port=80)
        return listener

    def create_fargate_task_definition(self):
        task_definition = ecs.FargateTaskDefinition(self, self.fargate_task_name, memory_limit_mib=1024, cpu=512)
        return task_definition

    def add_fargate_container_to_task(self):
        self.task_definition.add_container(self.fargate_container_name,
                                           image=ecs.ContainerImage.from_ecr_repository(self.ecr_repository, "latest"),
                                           memory_limit_mib=1024,
                                           cpu=512,
                                           port_mappings=[ecs.PortMapping(container_port=80)],
                                           container_name='app',
                                           logging=ecs.AwsLogDriver(
                                               stream_prefix='ecs',
                                               log_group=logs.LogGroup(
                                                   self, 'SportAppFrontendLogGroup',
                                                   log_group_name='/aws/ecs/SportAppFrontendTask',
                                               )
                                           ))

    def add_service_to_cluster(self):
        ecs_service = ecs.FargateService(self, self.fargate_service_name,
                                         cluster=self.cluster,
                                         task_definition=self.task_definition,
                                         desired_count=2
                                         )
        return ecs_service

    def create_log_policy_observability(self):
        log_policy = iam.Policy(
            self, "LogPolicy",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                    resources=[
                        f"arn:aws:logs:{self.region}:{self.account}:log-group:/ecs/{self.ecs_service.service_name}:*"
                    ]
                )
            ]
        )
        return log_policy

    def add_roles_to_task(self):
        self.ecs_service.task_definition.task_role.attach_inline_policy(self.log_policy)

    def add_listener_to_load_balancer(self):
        self.listener.add_targets("SportAppServiceTargets", port=80, targets=[self.ecs_service])

    def add_stage_to_pipeline(self):
        deploy_action = codepipeline_actions.EcsDeployAction(
            action_name="DeployECS",
            service=self.ecs_service,
            input=codepipeline.Artifact("imagedefinitions")
        )
        self.pipeline.add_stage(stage_name="Deploy", actions=[deploy_action])

    def grant_permissions_to_task(self):
        self.secret.grant_read(self.ecs_service.task_definition.task_role)
