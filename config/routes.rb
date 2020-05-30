Rails.application.routes.draw do
  resources :urls, only: [:create, :show], param: :code do
    resource :stats, only: [:show]
  end
end
