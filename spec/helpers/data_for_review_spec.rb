# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Booklog::Helpers do
  let(:context) { stub_template_context }
  describe '#data_for_review' do
    it 'returns a data hash for the given review' do
      book = OpenStruct.new(
        title: 'The Shining',
        year_published: '1977',
        sortable_title: 'Shining, The',
        isbn: '123456789'
      )

      review = OpenStruct.new(
        book_id: 'the-shining-by-stephen-king',
        date: '2011-03-12',
        grade: 'A+'
      )

      expect(context.data_for_review(book: book, review: review)).to eq(

        data: {
          title: 'The Shining',
          sort_title: 'Shining, The',
          isbn: '123456789',
          year_published: '1977',
          review_date: '2011-03-12',
          grade: '17'
        }
      )
    end
  end
end
