# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#data_for_review' do
    it 'returns a data hash for the given review' do
      review = OpenStruct.new(
        title: 'The Beyond (1980)',
        sortable_title: 'Beyond, The (1980)',
        release_date: Date.parse('1980-06-01'),
        date: '2011-03-12',
        grade: 'A+'
      )

      expect(context.data_for_review(review: review)).to eq(

        data: {
          title: 'The Beyond (1980)',
          sort_title: 'Beyond, The (1980)',
          release_date: '1980-06-01',
          release_date_year: 1980,
          review_date: '2011-03-12',
          grade: '17'
        }
      )
    end
  end
end
