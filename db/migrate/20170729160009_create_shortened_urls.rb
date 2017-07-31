class CreateShortenedUrls < ActiveRecord::Migration[5.1]
  def change
    create_table :shortened_urls do |t|
      t.string :url, null: false
      t.string :code, null: false
      t.integer :usage_count, default: 0
      t.datetime :last_usage

      t.timestamps
    end

    add_index :shortened_urls, :code, unique: true
  end
end
