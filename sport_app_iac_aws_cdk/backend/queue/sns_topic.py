from aws_cdk import Stack, aws_sns as sns
from constructs import Construct


class SnsTopic(Stack):
    def __init__(self, scope: Construct, stack_id: str, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.topic_name = "finish_training_sns"
        self.topic = self.create_sns_topic()

    def create_sns_topic(self):
        topic = sns.Topic(self, self.topic_name, display_name=self.topic_name)
        return topic
