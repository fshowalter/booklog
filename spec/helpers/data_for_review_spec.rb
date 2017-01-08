# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Booklog::Helpers do
  let(:context) { stub_template_context }
  describe '#data_for_review' do
    it 'returns a data hash for the given review' do
      review = OpenStruct.new(
        date: '2011-03-12',
        grade: 'A+',
        title_with_author: 'The Shining by Stephen King',
        year_published: '1977',
        sortable_title: 'Shining, The',
      )

      expect(context.data_for_review(review: review)).to eq(

        data: {
          title: 'The Shining by Stephen King',
          sort_title: 'Shining, The',
          year_published: '1977',
          review_date: '2011-03-12',
          grade: '17',
        },
      )
    end
  end
end
