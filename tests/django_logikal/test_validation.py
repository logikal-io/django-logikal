from pytest import raises
from pytest_mock import MockerFixture

from django_logikal.validation import ValidationMiddleware


def test_skipping(mocker: MockerFixture) -> None:
    request = mocker.Mock(
        headers={'Content-Type': 'text/html'},
        status_code=200,
        content=b'',
        resolver_match=mocker.Mock(app_name='test', route='test/'),
        path='/test/'
    )

    # No skipping
    middleware = ValidationMiddleware(get_response=lambda arg: arg)
    with raises(RuntimeError, match='Empty content'):
        middleware(request=request)

    # Skip app
    mocker.patch('django_logikal.validation.tool_config', return_value={
        'validate': {'skipped_apps': ['test']},
    })
    middleware = ValidationMiddleware(get_response=lambda arg: arg)
    middleware(request=request)  # does not raise an error

    # Skip route
    mocker.patch('django_logikal.validation.tool_config', return_value={
        'validate': {'skipped_routes': ['^test/.*']},
    })
    middleware = ValidationMiddleware(get_response=lambda request: request)
    middleware(request=request)  # does not raise an error
