# frozen_string_literal: true

class Url < ApplicationRecord
  before_validation :set_default_code

  validates :code, length: { maximum: 6 }
  validates :code, uniqueness: true
  validates :url, presence: true

  def visited
    update(
      last_usage: DateTime.now.in_time_zone('UTC'),
      usage_count: usage_count.to_i + 1
    )
  end

  private

  def set_default_code
    self.code = SecureRandom.alphanumeric(6) unless code
  end
end
