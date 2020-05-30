class CreateUrls < ActiveRecord::Migration[6.0]
  def change
    create_table :urls do |t|
      t.string :url, null: false
      t.string :code, index: true
      t.integer :usage_count, default: 0
      t.datetime :last_usage

      t.timestamps
    end
  end
end
