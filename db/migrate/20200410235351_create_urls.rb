# frozen_string_literal: true

class CreateUrls < ActiveRecord::Migration[6.0]
  def change
    create_table :urls do |t|
      t.string :url
      t.string :code
      t.datetime :last_usage
      t.integer :usage_count

      t.timestamps
    end
  end
end
