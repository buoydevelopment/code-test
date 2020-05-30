class StatsController < ApplicationController
  before_action :set_url, only: [:show]

  def show
    render json: {
      created_at: @url.created_at,
      last_usage: @url.last_usage,
      usage_count: @url.usage_count
    },
    status: :ok
  end

  private

  def set_url
    @url = Url.find_by!(code: params[:url_code])
  rescue ActiveRecord::RecordNotFound
    render status: :not_found
  end
end
