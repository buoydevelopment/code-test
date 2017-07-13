# spec/models/url_spec.rb
require 'rails_helper'

# Test suite for the URL model
RSpec.describe Url, type: :model do
  # ensure columns url and code are present before saving
  it { should validate_presence_of(:url) }
  it { should validate_presence_of(:code) }
end