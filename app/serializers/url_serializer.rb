# frozen_string_literal: true

class UrlSerializer
  include FastJsonapi::ObjectSerializer
  attributes :created_at, :last_usage, :usage_count
  attribute :last_usage, if: proc { |record| !record.last_usage.nil? }
end
