# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Booklog::Helpers do
  let(:context) { stub_template_context }
  describe '#data_for_author' do
    it 'returns a data hash for the given author' do
      author = OpenStruct.new(
        sortable_name: 'King, Stephen',
        name: 'Stephen King',
        reviews: [
          'title 1',
          'title 2'
        ]
      )

      expect(context.data_for_author(author: author)).to eq(
        data: {
          name: 'Stephen King',
          sort_name: 'King, Stephen',
          review_count: '002'
        }
      )
    end
  end
end
