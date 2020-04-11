# frozen_string_literal: true

require 'rails_helper'

RSpec.describe UrlSerializer, type: :serializer do
  describe 'Url is visited' do
    let(:url) { create(:url, :visited) }
    let(:url_serializer) { UrlSerializer.new(url) }

    it 'is last_usage present?' do
      hash_expected = {
        created_at: url.created_at,
        last_usage: url.last_usage,
        usage_count: url.usage_count
      }

      expect(url_serializer.serializable_hash[:data][:attributes])
        .to eq hash_expected
    end
  end

  describe 'Url is not visited' do
    let(:url) { create(:url) }
    let(:url_serializer) { UrlSerializer.new(url) }

    it 'is not last_usage present?' do
      hash_expected = {
        created_at: url.created_at,
        usage_count: url.usage_count
      }

      expect(url_serializer.serializable_hash[:data][:attributes])
        .to eq hash_expected
    end
  end
end
