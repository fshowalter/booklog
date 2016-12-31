# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#data_for_person' do
    it 'returns a data hash for the given person' do
      person = OpenStruct.new(
        full_name: 'Cushing, Peter',
        first_name: 'Peter',
        last_name: 'Cushing',
        performance_credits: [
          'title 1',
          'title 2'
        ]
      )

      expect(context.data_for_person(person: person, credits_method: :performance_credits)).to eq(
        data: {
          name: 'Peter Cushing',
          sort_name: 'Cushing, Peter',
          review_count: '002'
        }
      )
    end
  end
end
