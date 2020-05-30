class StatsController < ApplicationController
  before_action :set_url, only: [:show]

  def show
    render json: UrlSerializer.new(@url).serializable_hash[:data][:attributes], status: :ok
  end

  private

  def set_url
    @url = Url.find_by!(code: params[:code])
  rescue ActiveRecord::RecordNotFound
    render status: :not_found
  end
end
