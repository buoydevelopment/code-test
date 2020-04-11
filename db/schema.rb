# frozen_string_literal: true

ActiveRecord::Schema.define(version: 20_200_410_235_351) do
  create_table 'urls', force: :cascade do |t|
    t.string 'url'
    t.string 'code'
    t.datetime 'last_usage'
    t.integer 'usage_count'
    t.datetime 'created_at', precision: 6, null: false
    t.datetime 'updated_at', precision: 6, null: false
  end
end
