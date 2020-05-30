# frozen_string_literal: true

require 'rails_helper'

RSpec.describe Url, type: :model do
  describe '.generate_code' do
    describe 'When creating with code' do
      it 'uses the sent one' do
        code = "1code1"
        url = FactoryBot.create(:url, code: code)

        expect(url.code).to eq(code)
      end
    end

    describe 'When creating without code' do
      it 'uses the sent one' do
        url = FactoryBot.create(:url, :without_code)

        expect(url.code).not_to be_nil
      end
    end
  end

  describe '.add_visit' do
    let(:url) { FactoryBot.create(:url) }
    let(:old_count) { url.usage_count }

    it 'adds 1 to the usage counter' do
      expect { url.add_visit }.to change { url.reload.usage_count }.by(1)
    end

    it 'sets the last used date to now' do
      url.add_visit

      expect(url.reload.last_usage.round).to eq(DateTime.now.in_time_zone('UTC').round)
    end
  end
end