# frozen_string_literal: true

require 'rails_helper'

RSpec.describe StatsController, type: :request do
  describe '#show' do
    describe 'When the url is found' do
      it 'returns url stats' do
        url = create(:url)

        get url_stats_path(url.code)

        serialized_response = UrlSerializer.new(url).serializable_hash[:data][:attributes].to_json
        expect(response.body).to eq(serialized_response)
      end
    end

    describe 'When the url is not found' do
      it 'uses the sent one' do
        get url_stats_path('not_found')

        expect(response).to have_http_status(:not_found)
      end
    end
  end
end