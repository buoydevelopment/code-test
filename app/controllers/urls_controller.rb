class UrlsController < ApplicationController
  before_action :set_url, only: [:show]
  after_action :set_location_header, only: [:show]

  def create
    url = Url.create!(url_params)

    render json: {code: url.code}, status: :created
  rescue ActiveRecord::RecordInvalid
    render status: :conflict
  end

  def show
    @url.add_visit

    render status: :found
  end

  private

  def url_params
    params.permit(:url, :code)
  end

  def set_url
    @url = Url.find_by!(code: params[:code])
  rescue ActiveRecord::RecordNotFound
    render status: :not_found
  end

  def set_location_header
    response.headers['Location'] = @url.url
  end
end
