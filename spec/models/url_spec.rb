# frozen_string_literal: true

require 'rails_helper'

RSpec.describe Url, type: :model do
  describe 'validations' do
    subject { build(:url) }

    it { should validate_presence_of(:url) }
    it { should validate_uniqueness_of(:code) }
    it { should validate_length_of(:code).is_at_most(6) }
  end

  it '#set_default_code' do
    url = create(:url, :without_code)
    expect(url.code).not_to be_nil
  end
end
