import pytest
import mongoengine as me
from unittest.mock import patch
from falcon import testing
from botocore.stub import Stubber
from src import scrapinghub_helper, web


@pytest.fixture()
def web_app():
    return testing.TestClient(web.app)


@pytest.fixture(autouse=True)
def s3_stub():
    with Stubber(scrapinghub_helper.s3) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(autouse=True)
def mongo(request):
    me.connection.disconnect()
    db = me.connect('mongotest', host='mongomock://localhost')
