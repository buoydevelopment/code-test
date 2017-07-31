Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  resources :shortened_urls, only: :create, path: 'urls'
  get ':code' => 'shortened_urls#show', as: 'retrieve_url'
  get ':code/stats' => 'shortened_urls#stats', as: 'retrieve_stats'

end
