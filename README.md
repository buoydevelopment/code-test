MICROSERVICE PROJECT
**Installation instructions**
1) Clone the repo
    `git clone git@github.com:gnium/base-rails5-api.git`
2) Install dependant gems
    `bundle install`
3) Run tests 
    `bundle exec rspec`

**Service usage**
1) Start the server (default port is 3000)
    `rails s`
    if you run into any problem with ports, you can change it by run 
    `rails s -p 3001`
    where 3001 is the desired port
2) Url testing
    In postman: you can use GET/POST methods in order to get the following paths
    _**POST /urls**_
    `Content-Type: "application/json"  `
    `{
      "url": "http://example.com",
      "code": "example"
    }`
    _Params:_
    **url**: URL to shorten. Required
    **code**: Desired shortcode. Alphanumeric, case-sensitive 6 chars lenght.
    **Note**: If code is not provided, a random code, with the same constraints, must be generated

    _Response:_
    `201 Created`
    `Content-Type: "application/json"
    {
        "code": :shortcode
    }`
    _**Errors:**_
    
    **Bad Request**: If url is not present
    **Conflict**: If the the desired shortcode is already in use.
    **Unprocessable Entity**: If the shortcode doesn't doesn't comply with its description.

    _**GET /:code**_
    `Content-Type: "application/json"`
    _**Params:**_
    **code**: Encoded URL shortcode
    Response
    _It's a redirect response including the target URL in its Location header._
    `HTTP/1.1 302 Found`
    `Location: http://www.example.com`
    _**Errors**_
    **Not Found:** If the shortcode cannot be found

    _**GET /:code/stats**_
`Content-Type: "application/json"`

    _Params:_

    **code**: Encoded URL shortcode

    Response
    `200 OK`
    `Content-Type: "application/json"`
    `{
      "created_at": "2012-04-23T18:25:43.511Z",
      "last_usage": "2012-04-23T18:25:43.511Z",
      "usage_count": 1
    }`
    
    **start_date**: ISO8601 formatted date when the shortened URL was created
    **usage_count**: Number of requests to the endpoint GET /code
    **last_usage**: Date of the last time the shortened URL was requested. Not included if it has never been requested.
Errors

    **Not Found**: If the shortcode cannot be found
