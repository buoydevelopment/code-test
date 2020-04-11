# frozen_string_literal: true

class StatsController < ApplicationController
  def show
    @url = Url.find_by_code(params[:code])
    render json: UrlSerializer.new(@url).serializable_hash[:data][:attributes]
  end
end
