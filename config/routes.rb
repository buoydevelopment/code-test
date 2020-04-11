# frozen_string_literal: true

Rails.application.routes.draw do
  post 'urls', to: 'urls#create'
  get '/:code', to: 'urls#show', as: 'url'
  get '/:code/stats', to: 'stats#show', as: 'url_stats'
end
