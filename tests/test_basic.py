from api.models import db, Code
import base64
import re


# Test the common way to insert a url
def test_post_url_and_code(client):
    rs = client.post("/urls", json={
        "url": "https://www.testdb.com",
        "code": "code01"
    })

    json_data = rs.get_json()
    assert json_data['code'] == base64.urlsafe_b64encode(b'code01').decode('ascii')
    assert rs.status_code == 201

# Test insert a url without a code
def test_post_url(client):
    rs = client.post("/urls", json={
        "url": "https://www.testdb.com"
    })

    json_data = rs.get_json()
    generated_code =  base64.urlsafe_b64decode(json_data['code']).decode('ascii')
    assert len(generated_code) == 6
    assert re.match('[A-Za-z0-9]', generated_code)
    assert rs.status_code == 201

# Test the retrieve of the url
def test_get_url(client):
    url = "https://www.testdb.com"
    rs = client.post("/urls", json={
        "url": url,
        "code": "code02"
    })

    rs_data = rs.get_json()

    rv = client.get("/" + rs_data['code'])
    rv_data = rv.get_json()
    assert rv_data['url'] == url
    assert rs.status_code == 201
    assert rv.status_code == 302

# Test the retrieve of the stats of an url
def test_get_url_stats(client):
    # this assume the run of the previous test
    code = base64.urlsafe_b64encode(b'code02').decode('ascii')
    rv = client.get("/" + code + '/stats')
    rv_data = rv.get_json()
    assert 'created_at' in rv_data
    assert 'last_usage' in rv_data
    assert 'usage_count' in rv_data
    assert rv_data['usage_count'] == 1
    assert rv.status_code == 200

    # this assume the run of the first test
    code = base64.urlsafe_b64encode(b'code01').decode('ascii')
    rs = client.get("/" + code + '/stats')
    rs_data = rs.get_json()
    assert 'created_at' in rs_data
    assert 'last_usage' not in rs_data
    assert 'usage_count' in rs_data
    assert rs_data['usage_count'] == 0
    assert rs.status_code == 200

# Test the common errors to insert a url
def test_post_bad_code(client):
    rs = client.post("/urls", json={
        "url": "https://www.testdb.com",
        "code": "code0103"
    })

    json_data = rs.get_json()
    assert 'error' in json_data
    assert rs.status_code == 422

# Test the common errors to insert a url
def test_post_existent_code(client):
    rs = client.post("/urls", json={
        "url": "https://www.testdb.com",
        "code": "code01"
    })

    json_data = rs.get_json()
    assert 'error' in json_data
    assert rs.status_code == 409

# Test the common errors to insert a url
def test_post_without_url(client):
    rs = client.post("/urls", json={
        "code": "code03"
    })

    json_data = rs.get_json()
    assert 'error' in json_data
    assert rs.status_code == 400

# Test the not found code
def test_get_not_found_code(client):
    code = base64.urlsafe_b64encode(b'code03').decode('ascii')
    rs = client.get("/" + code)

    json_data = rs.get_json()
    assert 'error' in json_data
    assert rs.status_code == 404

# Test the not found stats
def test_get_not_found_code(client):
    code = base64.urlsafe_b64encode(b'code03').decode('ascii')
    rs = client.get("/" + code + '/stats')

    json_data = rs.get_json()
    assert 'error' in json_data
    assert rs.status_code == 404
