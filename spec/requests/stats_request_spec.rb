# frozen_string_literal: true

require 'rails_helper'

RSpec.describe 'Stats', type: :request do
  describe 'GET show' do
    let(:url) { create(:url) }
    before { get url_stats_path(url.code) }

    it { expect(response).to have_http_status(:success) }

    it 'return UrlSerializer' do
      serializer = UrlSerializer.new(url).serializable_hash[:data][:attributes]
      expect(response.body).to eq serializer.to_json
    end
  end
end
