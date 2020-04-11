# frozen_string_literal: true

FactoryBot.define do
  factory :url do
    url { 'http://example.com' }
    code { 'exmple' }

    trait :without_code do
      code { nil }
    end

    trait :visited do
      last_usage { DateTime.now }
      usage_count { 1 }
    end
  end
end
