import json
from behave import when, then
from shorter_app.apis.shorter_api import generate_shortcode
from shorter_app.validator import (
    ERROR_INVALID_CODE,
    ERROR_DUPLICATED_CODE,
    ERROR_INVALID_URL,
    ERROR_CODE_NOT_FOUND,
    ERROR_URL_IS_REQUIRED,
)


@when("I test healthcheck")
def step_impl(context):
    response = context.client.get("/shorter/healthcheck/")
    context.response = response


@then("I get status code {status_code}")
def step_impl(context, status_code):
    assert int(status_code) == context.response.status_code


@then("the value for location header is {url}")
def test_get_code(context, url):
    assert context.response.headers.get("location") == url


@then("the value of {attribute} is {value}")
def step_impl(context, attribute, value):
    if attribute in ["created_at", "last_usage"]:
        assert json.loads(context.response.data).get(attribute)
    elif attribute == "usage_count":
        assert json.loads(context.response.data).get(attribute) == value
    else:
        if value == "ERROR_INVALID_CODE":
            value = ERROR_INVALID_CODE
        if value == "ERROR_DUPLICATED_CODE":
            value = ERROR_DUPLICATED_CODE
        if value == "ERROR_INVALID_URL":
            value = ERROR_INVALID_URL
        if value == "ERROR_CODE_NOT_FOUND":
            value = ERROR_CODE_NOT_FOUND
        if value == "ERROR_URL_IS_REQUIRED":
            value = ERROR_URL_IS_REQUIRED

        assert json.loads(context.response.data).get(attribute) == value


@when("I post a valid short URL with a valid code")
def test_post_ok(context):
    context.code = generate_shortcode()
    response = context.client.post(
        "/shorter/urls/", json={"url": "http://url.com", "code": context.code}
    )
    context.response = response


@when("I post a valid short URL with a valid code and URL {url}")
def test_post_ok(context, url):
    context.code = generate_shortcode()
    response = context.client.post(
        "/shorter/urls/", json={"url": url, "code": context.code}
    )
    context.response = response


@then("the code is correct")
def step_impl(context):
    code = json.loads(context.response.data).get("code")
    assert code == context.code


@when("I post a valid short URL without code")
def test_post_ok_without_code(context):
    response = context.client.post("/shorter/urls/", json={"url": "http://url.com"})
    context.response = response
    context.code = json.loads(response.data).get("code")


@when("I post an invalid URL")
def test_post_invalid_url(context):
    response = context.client.post("/shorter/urls/", json={"url": "XXX"})
    context.response = response


@when("I post a missing URL")
def test_post_invalid_url(context):
    response = context.client.post("/shorter/urls/", json={"invalid_field": "XXX"})
    context.response = response


@when("I post an invalid code")
def test_post_invalid_shortcode(context):
    response = context.client.post(
        "/shorter/urls/", json={"url": "http://url.com", "code": "$%$^$%&"}
    )
    context.response = response


@when("I post a valid short URL with the same valid code")
def test_post_duplicated_shortcode(context):
    code = context.code
    response = context.client.post(
        "/shorter/urls/", json={"url": "http://url.com", "code": code}
    )
    context.response = response


@when("I get the same valid code")
def test_get_code(context):
    code = context.code
    response = context.client.get(f"/shorter/urls/{code}/")
    context.response = response


@when("I get an invalid code")
def test_get_url_invalid_code(context):
    response = context.client.get("/shorter/urls/XXXX/")
    context.response = response


@when("I get code stats")
def test_get_code_stats(context):
    code = context.code
    response = context.client.get(f"/shorter/urls/{code}/stats/")
    context.response = response


@when("I get invalid code stats")
def test_get_invalid_code_stats(context):
    response = context.client.get("/shorter/urls/XXXX/stats/")
    context.response = response


@when("I get a valid short URL with a valid code")
def test_get_invalid_code_stats(context):
    response = context.client.get("/shorter/urls/")
    context.response = response
