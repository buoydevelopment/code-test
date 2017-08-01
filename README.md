# Code-Test Implementation by Pablo Cordero

### Background

This is a simple implementation of a URL Shortener service that allows user to submit a URL and get a code and shorter URL in return.

### Installation

1) Clone this repository:
```
	git clone git@github.com:pcordero/code-test.git
```
2) Install required gems
```
	bundle install
```
3) Start application
```
	bundle exec rails server
```

### Features

_**POST /urls**_

Submit an URL to get a shortcode

PARAMETERS
```
{
  url: 'http://www,.example.com',
  code: 'testcd' # optional, 6-character long
}
```

Test with : 
```
curl -H "Content-Type: application/json" -X POST -d '{"url":"http://www.example.com","code":"testcd"}' http://localhost:3000/urls
```


_**POST /[code]**_

Submit an URL to get a shortcode

PARAMETERS
```
{
  code: 'testcd'
}
```

Test with:
```
curl -H "Content-Type: application/json" -X GET http://localhost:3000/testcd -L
````

_**POST /[code]/stats**_

Submit an URL to get a shortcode

PARAMETERS
```
{
  code: 'testcd'
}
```

Test with:
```
curl -H "Content-Type: application/json" -X GET http://localhost:3000/testcd/stats
```

### Rationale & Potential enhancements

The task was implemented as a Rails API as it's the technology I know best and feel more comfortable with. Being this a test and with a limited functionality I implemented all actions on a single controller, it it were more complex and perhaps we were collecting and doing some other things with the stats, I would extract a StatsController.

I am letting the UrlShortener model take care of the validations, in the controller I am reading the error messages to determine the status code to return to the client. If we were using more status codes that could make things more complex on the controller, but for this test I thougt it would be best to leveraga the ActiveRecord validations.

The first improvement I would look into for this test is validating the correctness of the URL, right now it accepts any string from the user.

