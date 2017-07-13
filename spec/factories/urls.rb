FactoryGirl.define do
  factory :url do
    url { Faker::Lorem.word }
    code { Faker::Lorem.characters(10) }
  end
end