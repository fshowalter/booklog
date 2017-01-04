# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Booklog::Helpers do
  let(:context) { stub_template_context }
  describe '#data_for_reading' do
    it 'returns a data hash for the given reading' do
      reading = OpenStruct.new(
        date_started: '2011-11-04',
        date_finished: '2011-11-06'
      )

      book = OpenStruct.new(
        title: 'The Shining',
        isbn: '0451150325',
        sortable_title: 'Shining, The',
        year_published: 1977
      )

      expect(context.data_for_reading(book: book, reading: reading)).to eq(
        data: {
          title: 'The Shining',
          isbn: '0451150325',
          sort_title: 'Shining, The',
          year_published: 1977,
          date_started: '2011-11-04',
          date_finished: '2011-11-06'
        }
      )
    end
  end
end
