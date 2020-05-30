class Url < ApplicationRecord
  before_create :generate_code, if: Proc.new { |url| url.code.blank? }

  validates :url, presence: true
  validates :code,
    length: { maximum: 6 },
    uniqueness: true

  def add_visit
    self.last_usage = DateTime.now
    self.usage_count += 1

    self.save
  end

  private

  def generate_code
    self.code = SecureRandom.uuid[0..5]
  end
end
