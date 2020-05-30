Rails.application.routes.draw do
  resources :urls, only: [:create, :show], param: :code
  get ':code/stats', to: 'stats#show', as: :url_stats
end
