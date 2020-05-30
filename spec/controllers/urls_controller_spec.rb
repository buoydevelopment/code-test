# frozen_string_literal: true

require 'rails_helper'

RSpec.describe UrlsController, type: :request do
  describe '#create' do
    describe 'When the params are valid' do
      let(:valid_params) {{url: 'www.example.com', code: 'valid1'}}

      it 'creates the url' do
        expect { post urls_path, params: valid_params }.to change { Url.count }.by(1)
      end

      it 'returns the url code' do
        post urls_path, params: valid_params

        expect(response.body).to eq({"code": valid_params[:code]}.to_json)
      end

      it 'returns an ok status' do
        post urls_path, params: valid_params

        expect(response).to have_http_status(:created)
      end
    end

    describe 'When the params are invalid' do
      let(:invalid_params) {{url: nil, code: 'too_large'}}

      it 'returns a conflict status' do
        post urls_path, params: invalid_params

        expect(response).to have_http_status(:conflict)
      end
    end
  end

  describe '#show' do
    describe 'When the url is not found' do
      it 'uses the sent one' do
        get url_path('not_found')

        expect(response).to have_http_status(:not_found)
      end
    end

    describe 'When the url is found' do
      let(:url) { FactoryBot.create(:url) }

      it 'adds 1 visit to the url' do
        expect { get url_path(url.code) }.to change { url.reload.usage_count }.by(1)
      end

      it 'sets last_usage to now' do
        get url_path(url.code)

        expect(url.reload.last_usage.round).to eq(DateTime.now.in_time_zone('UTC').round)
      end

      it 'sets the location header to the url' do
        get url_path(url.code)

        expect(response.headers['Location']).to eq(url.url)
      end

      it 'returns a found status' do
        get url_path(url.code)

        expect(response).to have_http_status(:found)
      end
    end
  end
end