class ShortenedUrl < ApplicationRecord
  validates :url, :code, presence: true
  validates :code, uniqueness: true, length: { is: 6 }, format: { with: /\A[A-Za-z0-9]+\z/ }

  before_validation :check_code, on: :create

  private
    def check_code
      self.code = loop do
        random_code = SecureRandom.urlsafe_base64(4)
        break random_code unless %w(- _).any?{ |c| random_code.include?(c)} || self.class.exists?(code: random_code)
      end if code.blank?
    end
end
