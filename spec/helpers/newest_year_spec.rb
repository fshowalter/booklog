# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#newest_year' do
    it 'returns the newest year for the given collection and year method' do
      viewings = [
        OpenStruct.new(date: Date.parse('2011-03-12')),
        OpenStruct.new(date: Date.parse('1976-03-12')),
        OpenStruct.new(date: Date.parse('2000-01-10'))
      ]

      expect(context.newest_year(collection: viewings, date_method: :date)).to eq(2011)
    end
  end
end
