require 'test_helper'

class ShortenedUrlsControllerTest < ActionDispatch::IntegrationTest
  test "it returns 'bad request' if url is not present" do
    post shortened_urls_path, params: {
                                shortened_url: {
                                  code: 'code01'
                                }
                              }

    assert_response :bad_request
  end

  test "it returns 'conflict' if code is arleady taken" do
    post shortened_urls_path, params: {
                                shortened_url: {
                                  url: 'http://www,example.com',
                                  code: 'github'
                                }
                              }

    assert_response :conflict
  end

  test "it returns 'unprocessable entity' if code is invalid" do
    post shortened_urls_path, params: {
                                shortened_url: {
                                  url: 'http://www,example.com',
                                  code: 'shortcode'
                                }
                              }

    assert_response :unprocessable_entity
  end

  test "providing valid parameters, a new url is created" do
    post shortened_urls_path, params: {
                                shortened_url: {
                                  url: 'http://www,example.com',
                                  code: '123456'
                                }
                              }


    assert_response :success
  end

  test "it generates a code if one is not provided" do
    post shortened_urls_path, params: {
                                shortened_url: {
                                  url: 'http://www,example.com'
                                }
                              }


    assert_response :success

    data = JSON.parse response.body
    assert data['code'].present?
  end

  test "with a valid code it redirects to the corrresponding url" do
    assert_difference 'ShortenedUrl.find_by(code: "upwork").usage_count', 1 do
      get retrieve_url_path('upwork')
    end

    assert_response :redirect
  end

  test "it returns 'not found' if code does not exist" do
    get retrieve_url_path('twittr')

    assert_response :not_found
  end

  test "with a valid code it retrives stats" do

    get retrieve_stats_path('upwork')

    assert_response :success
  end

  test "it returns 'not found' if getting stats for an invalid code" do
    get retrieve_url_path('twittr')

    assert_response :not_found
  end



end
