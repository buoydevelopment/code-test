class ShortenedUrlsController < ApplicationController

  def create
    @shortened_url = ShortenedUrl.new(shortened_url_params)

    if @shortened_url.save
      render json: @shortened_url.to_json(only: [:code]), status: :created
    else
      render json: @shortened_url.errors, status: status_from_errors(@shortened_url.errors)
    end

  end

  def show
    begin
      @shortened_url = ShortenedUrl.find_by!(code: params[:code])
      @shortened_url.touch(:last_usage)
      ShortenedUrl.increment_counter(:usage_count, @shortened_url.id)
      render @shortened_url, status: :found, location: @shortened_url.url
    rescue ActiveRecord::RecordNotFound
      render status: :not_found
    end
  end

  def stats
    begin
      @shortened_url = ShortenedUrl.find_by!(code: params[:code])
      fields = [:created_at, :usage_count]
      fields << :last_usage if !@shortened_url.last_usage.nil?
      render json: @shortened_url.to_json(only: fields)
    rescue ActiveRecord::RecordNotFound
      render status: :not_found
    end
  end

  private

    def shortened_url_params
      params.require(:shortened_url).permit(:url, :code)
    end

    def status_from_errors(errors)
      first_error = errors.details.first.flatten
      error_field = first_error[0]
      failed_validation = first_error[1][:error]

      if error_field == :url && failed_validation == :blank
        :bad_request
      elsif error_field == :code && failed_validation == :taken
        :conflict
      else
        :unprocessable_entity
      end
    end
end
