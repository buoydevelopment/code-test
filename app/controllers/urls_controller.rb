class UrlsController < ApplicationController
  def create
    url = Url.create(url_params)

    render json: {code: url.code}, status: :created
  end

  private

  def url_params
    params.permit(:url, :code)
  end
end
