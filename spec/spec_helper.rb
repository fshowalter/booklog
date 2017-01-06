# frozen_string_literal: true
require 'simplecov'
SimpleCov.start do
  add_filter '/vendor/'
  add_filter '/extensions/'
end

require 'bundler/setup'
Bundler.require

require 'rspec'

RSpec.configure do |config|
  config.order = 'random'
end

require_relative '../booklog/booklog'

require 'fakeweb'
FakeWeb.allow_net_connect = false
