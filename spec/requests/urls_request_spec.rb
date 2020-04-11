# frozen_string_literal: true

require 'rails_helper'

RSpec.describe 'Urls', type: :request do
  describe 'POST /create' do
    let(:valid_params) { { url: 'http://example.com', code: 'exmple' } }

    it 'check create a new Url' do
      expect { post urls_path, params: valid_params }
        .to change { Url.count }.by(1)
    end

    context 'with valid params' do
      let(:last_url) { Url.last }
      before { post urls_path, params: valid_params }

      it { expect(response).to have_http_status(201) }
      it { expect(last_url.url).to eq(valid_params[:url]) }
      it { expect(last_url.code).to eq(valid_params[:code]) }
      it { expect(JSON.parse(response.body)['code']).to eq valid_params[:code] }
    end

    context 'with valid params' do
      let(:invalid_params) { { code: 'example' } }
      before { post urls_path, params: invalid_params }

      it { expect(response).to have_http_status(400) }
    end
  end

  describe 'GET /:code' do
    let!(:new_url) { create(:url) }

    it 'check usage_count increment updated' do
      expect { get url_path(new_url.code) }
        .to change { new_url.reload.usage_count }.from(nil).to(1)
    end

    context 'with valid params' do
      before { get url_path(new_url.code) }

      it { expect(response).to have_http_status(302) }
      it 'Location header?' do
        expect(response.headers['Location']).to eq new_url.url
      end

      it 'check last_usage was updated' do
        expect(new_url.reload.last_usage.round)
          .to eq DateTime.now.in_time_zone('UTC').round
      end
    end

    context 'with invalid params' do
      before { get url_path('not_code') }
      it { expect(response).to have_http_status(400) }
    end
  end
end
