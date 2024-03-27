from aws_cdk import Stack, aws_sns as sns, aws_sns_subscriptions as sns_subs, aws_sqs as sqs, aws_lambda as _lambda
from constructs import Construct


class Sqs(Stack):

    def __init__(self, scope: Construct, stack_id: str, sns_service: sns, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.sns_service = sns_service
        self.queue_name = "finish_training_queue.fifo"
        self.lambda_name = "finish_training_sns_lambda"
        self.lambda_event_source_mapping_name = "finish_training_sns_lambda_event_source"
        self.queue = self.create_sqs()
        self.sqs_subscription = self.create_sqs_subscription()
        self.create_sns_subscription()
        self.create_lambda()

    def create_sqs(self):
        queue = sqs.Queue(self, self.queue_name, queue_name=self.queue_name, fifo=True)
        return queue

    def create_sqs_subscription(self):
        sqs_subscription = sns_subs.SqsSubscription(self.queue)
        return sqs_subscription

    def create_sns_subscription(self):
        self.sns_service.topic.add_subscription(self.sqs_subscription)

    def create_lambda(self):
        lambda_function = _lambda.Function(self, self.lambda_name,
                                           runtime=_lambda.Runtime.PYTHON_3_11,
                                           handler="index.handler",
                                           code=_lambda.Code.from_inline(
                                               code='def handler(event, context): return print(event)'))

        self.queue.grant_consume_messages(lambda_function)

        _lambda.EventSourceMapping(self, self.lambda_event_source_mapping_name,
                                   target=lambda_function,
                                   batch_size=1,
                                   event_source_arn=self.queue.queue_arn,
                                   )
