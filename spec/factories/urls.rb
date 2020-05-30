FactoryBot.define do
  factory :url do
    url { "www.example.com" }
    code {'exampl'}

    trait :without_code do
      code { nil }
    end

    trait :with_invalid_code do
      code {'invalid'}
    end
  end
end