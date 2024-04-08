from aws_cdk import (Stack, aws_codepipeline as codepipeline, aws_codepipeline_actions as codepipeline_actions,
                     aws_codebuild as codebuild, aws_ecr as ecr, Fn)
from constructs import Construct


class UserBackendEcrPipeline(Stack):
    def __init__(self, scope: Construct, stack_id: str, docker_hub_secret, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.id = stack_id
        self.docker_hub_secret = docker_hub_secret
        self.connection_code_start_arn = ("arn:aws:codestar-connections:us-east-1:767398152758:connection/"
                                          "57c79685-ad89-4f71-9a22-8cdb670e6f86")
        self.repo_owner = 'sport-app-team-5'
        self.repo_name = 'user_sport_app'
        self.repo_branch = 'main'
        self.codepipeline_name = 'user_backend_pipeline'
        ecr_repository_name = Fn.import_value('UserBackendEcrCfnOutput')
        self.ecr_repository = ecr.Repository.from_repository_name(self, ecr_repository_name, ecr_repository_name)

        self.codebuild_project = self.create_pipeline()
        self.grant_permissions_to_dockerhub()
        self.source_action, self.source_output = self.add_source_stage()
        self.build_action = self.add_build_stage()
        self.pipeline = self.add_stages_to_pipeline()

    def create_pipeline(self):
        code_build_constr_id = self.id + "-codebuild-id"
        code_build_project_name = self.id
        codebuild_project = codebuild.PipelineProject(
            self, code_build_constr_id, project_name=code_build_project_name,
            environment=codebuild.BuildEnvironment(privileged=True),
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "pre_build": {
                        "commands": [
                            '$(aws secretsmanager get-secret-value --secret-id $SECRET_ARN --query SecretString '
                            '--output text > docker_hub_creds.json)'.format(self.docker_hub_secret),
                            'USERNAME=$(jq -r ".USERNAME" docker_hub_creds.json)',
                            'TOKEN=$(jq -r ".TOKEN" docker_hub_creds.json)',
                            'echo $TOKEN | docker login -u $USERNAME --password-stdin'
                        ]
                    },
                    "build": {
                        "commands": [
                            "$(aws ecr get-login --region $AWS_DEFAULT_REGION --no-include-email)",
                            "docker build -t $REPOSITORY_URI:latest . ",
                            "docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION"
                        ]
                    },
                    "post_build": {
                        "commands": [
                            "docker push $REPOSITORY_URI:latest",
                            "docker push $REPOSITORY_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION",
                            "export imageTag=$CODEBUILD_RESOLVED_SOURCE_VERSION",
                            "printf '[{\"name\":\"app\",\"imageUri\":\"%s\"}]' $REPOSITORY_URI:$imageTag "
                            "> imagedefinitions.json"
                        ]
                    }
                },
                "env": {"exported-variables": ["imageTag"]},
                "artifacts": {
                    "files": "imagedefinitions.json",
                    "secondary-artifacts": {
                        "imagedefinitions": {
                            "files": "imagedefinitions.json",
                            "name": "imagedefinitions"
                        }}}
            }),
            environment_variables={
                "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(value=self.ecr_repository.repository_uri),
                "SECRET_ARN": codebuild.BuildEnvironmentVariable(value=self.docker_hub_secret.secret_full_arn)
            })
        return codebuild_project

    def grant_permissions_to_dockerhub(self):
        self.docker_hub_secret.grant_read(self.codebuild_project.role)
        self.ecr_repository.grant(self.codebuild_project, "ecr:GetAuthorizationToken")
        self.ecr_repository.grant_pull_push(self.codebuild_project)

    def add_source_stage(self):
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHub_Source",
            connection_arn=self.connection_code_start_arn,
            owner=self.repo_owner,
            repo=self.repo_name,
            branch=self.repo_branch,
            output=source_output
        )
        return source_action, source_output

    def add_build_stage(self):
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=self.codebuild_project,
            input=self.source_output,
            outputs=[codepipeline.Artifact("imagedefinitions")],
            execute_batch_build=False
        )
        return build_action

    def add_stages_to_pipeline(self):
        pipeline_constr_id = self.id + "-codepipeline-id"

        pipeline = codepipeline.Pipeline(self, pipeline_constr_id, pipeline_name=self.codepipeline_name,
                                         stages=[
                                             {
                                                 "stageName": "Source",
                                                 "actions": [self.source_action]
                                             },
                                             {
                                                 "stageName": "Build",
                                                 "actions": [self.build_action]
                                             }
                                         ])
        return pipeline
