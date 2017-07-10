# Code Challenge

Create a micro service to shorten urls like bit.ly or TinyURL do.

## Rules

1. The service must expose HTTP endpoints according to the API Docs below.
2. Use your technology of choice, there's no restrictions. Instructions for the installation must be detailed in the INSTALL.md file.
3. Write the tests you consider necessary.

-------------------------------------------------------------------------

## API Docs

### POST /urls

```
POST /urls
Content-Type: "application/json"

{
  "url": "http://example.com",
  "code": "example"
}
```

##### Params:

* **url**: URL to shorten. Required
* code: Desired shortcode. Alphanumeric, case-sensitive 6 chars lenght.

Note: If code is not provided, a random code, with the same constraints, must be generated

##### Response:

```
201 Created
Content-Type: "application/json"

{
  "code": :shortcode
}
```

##### Errors:

* Bad Request: If ```url``` is not present
* Conflict: If the the desired shortcode is already in use.
* Unprocessable Entity: If the shortcode doesn't doesn't comply with its description.


### GET /:code

```
GET /:code
Content-Type: "application/json"
```

##### Params:
* **code**:  Encoded URL shortcode

##### Response

It's a redirect response including the target URL in its `Location` header.

```
HTTP/1.1 302 Found
Location: http://www.example.com
```

##### Errors

* Not Found: If the `shortcode` cannot be found

### GET /:code/stats

```
GET /:code/stats
Content-Type: "application/json"
```

##### Params:
* **code**:  Encoded URL shortcode

##### Response

```
200 OK
Content-Type: "application/json"

{
  "created_at": "2012-04-23T18:25:43.511Z",
  "last_usage": "2012-04-23T18:25:43.511Z",
  "usage_count": 1
}
```

* **`start_date`**: [ISO8601](http://en.wikipedia.org/wiki/ISO_8601) formatted date when the shortened URL was created
* **`usage_count`**: Number of requests to the endpoint `GET /code`
* `last_usage`: Date of the last time the shortened URL was requested. Not included if it has never been requested.

##### Errors

* Not Found: If the `shortcode` cannot be found
