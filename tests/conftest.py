import os
import json
from unittest.mock import MagicMock
import pytest
from aws_cdk import Environment
import aws_cdk as core


class Conftest:
    def get_cdk_json(self):
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, '../.', 'cdk.json')

        with open(json_path, 'r') as json_file:
            json_content = json.load(json_file)

        return json_content

    def get_env(self):
        context = self.get_cdk_json()['context']
        env = Environment(account=context['aws_account'], region=context['aws_region'])
        return env


@pytest.fixture(scope="function")
def app():
    _app = core.App()
    yield _app


@pytest.fixture(scope="function")
def env():
    _env = Conftest().get_env()
    yield _env


@pytest.fixture()
def docker_hub_secret_mock():
    docker_hub_secret_mock = MagicMock()
    docker_hub_secret_mock.secret_full_arn = "secret"
    return docker_hub_secret_mock
