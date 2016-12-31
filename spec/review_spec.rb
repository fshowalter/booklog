# frozen_string_literal: true
require 'spec_helper'

describe Movielog::Review do
  describe '#title_without_year' do
    it 'returns the title without the year' do
      review = Movielog::Review.new(title: 'Fright Night (1985)')
      expect(review.title_without_year).to eq 'Fright Night'
    end

    describe 'when year has roman numeral annotation' do
      it 'returns the title without the year' do
        review = Movielog::Review.new(title: 'She (1965/I)')
        expect(review.title_without_year).to eq 'She'
      end
    end
  end

  describe '#year' do
    it 'returns the year' do
      review = Movielog::Review.new(db_title: 'Fright Night (1985)')
      expect(review.year).to eq '1985'
    end

    describe 'when year has roman numeral annotation' do
      it 'returns the year without annotation' do
        review = Movielog::Review.new(db_title: 'She (1965/I)')
        expect(review.year).to eq '1965'
      end
    end
  end
end
