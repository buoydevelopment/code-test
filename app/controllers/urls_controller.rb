# frozen_string_literal: true

class UrlsController < ApplicationController
  after_action :set_location

  def show
    @url = Url.find_by_code(params[:code])
    if @url
      @url.visited
      render status: 302
    else
      render status: 400
    end
  end

  def create
    @url = Url.create(url_params)

    if @url.valid?
      render json: { code: @url.code }, status: 201
    else
      render status: 400
    end
  end

  private

  def url_params
    params.permit(:url, :code)
  end

  def set_location
    response.headers['Location'] = @url.url if @url
  end
end
