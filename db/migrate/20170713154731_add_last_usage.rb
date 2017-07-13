class AddLastUsage < ActiveRecord::Migration[5.0]
  def change
    add_column :urls, :last_usage, :timestamp
  end
end
