class AddUsageStatistics < ActiveRecord::Migration[5.0]
  def change
    add_column :urls, :views_count, :integer
  end
end
