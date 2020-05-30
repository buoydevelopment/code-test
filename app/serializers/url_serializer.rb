class UrlSerializer
  include FastJsonapi::ObjectSerializer

  attributes :created_at, :usage_count

  attribute :last_usage, if: Proc.new { |record| !record.last_usage.nil? }
end
