# frozen_string_literal: true
require 'spec_helper'

describe Booklog do
  describe '#site_url' do
    it 'returns the site url' do
      expect(Booklog.site_url).to eq 'https://booklog.frankshowalter.com'
    end
  end

  describe '#site_title' do
    it 'returns the site title' do
      expect(Booklog.site_title).to eq "Frank's Book Log"
    end
  end

  describe '#site_tagline' do
    it 'returns the site tagline' do
      expect(Booklog.site_tagline).to eq "Literature is a Relative Term"
    end
  end

  describe '#next_reading_sequence' do
    it 'returns the length of readings plus one' do
      expect(Booklog).to(receive(:readings)) do
        {
          1 => OpenStruct.new(sequence: 3),
          2 => OpenStruct.new(sequence: 1)
        }
      end

      expect(Booklog.next_reading_sequence).to eq 3
    end
  end

  describe '#next_review_sequence' do
    it 'returns the length of reviews plus one' do
      expect(Booklog).to(receive(:reviews)) do
        {
          1 => OpenStruct.new(sequence: 3),
          2 => OpenStruct.new(sequence: 1)
        }
      end

      expect(Booklog.next_review_sequence).to eq 3
    end
  end

  describe '#books' do
    it 'calls Booklog::ParseBooks' do
      expect(Booklog::ParseBooks).to(receive(:call)).and_return('parse data')

      expect(Booklog.books).to eq 'parse data'
    end
  end

  describe '#pages' do
    it 'calls Booklog::ParsePages' do
      expect(Booklog::ParsePages).to(receive(:call)).and_return('parse data')

      expect(Booklog.pages).to eq 'parse data'
    end
  end

  describe '#reviews' do
    it 'calls Booklog::ParseReviews' do
      expect(Booklog::ParseReviews).to(receive(:call)).and_return('parse data')

      expect(Booklog.reviews).to eq 'parse data'
    end

    describe 'when #cache_reviews is true' do
      before(:each) do
        Booklog.cache_reviews = true
      end

      after(:each) do
        Booklog.cache_reviews = false
      end

      it 'caches reviews' do
        expect(Booklog::ParseReviews).to(receive(:call)).and_return('parse data')

        expect(Booklog.reviews).to eq 'parse data'

        expect(Booklog.instance_variable_get('@reviews')).to eq 'parse data'
      end
    end
  end

  describe '#readings' do
    it 'calls Booklog::ParseReadings' do
      expect(Booklog::ParseReadings).to(receive(:call)).and_return('parse data')

      expect(Booklog.readings).to eq 'parse data'
    end
  end

  describe '#reviews_by_sequence' do
    it 'returns the reviews sorted by sequence in reverse' do
      expect(Booklog).to(receive(:reviews)) do
        {
          'isbn 1' => OpenStruct.new(isbn: 'isbn 1', sequence: 2),
          'isbn 2' => OpenStruct.new(isbn: 'isbn 2', sequence: 1)
        }
      end

      reviews_by_sequence = Booklog.reviews_by_sequence

      expect(reviews_by_sequence.first.isbn).to eq('isbn 1')
      expect(reviews_by_sequence.last.isbn).to eq('isbn 2')
    end

    describe 'when #cache_reviews is true' do
      before(:each) do
        Booklog.cache_reviews = true
      end

      after(:each) do
        Booklog.cache_reviews = false
      end

      it 'caches reviews_by_sequence' do
        expect(Booklog).to(receive(:reviews)) do
          {
            'isbn 1' => OpenStruct.new(isbn: 'isbn 1', sequence: 2),
            'isbn 2' => OpenStruct.new(isbn: 'isbn 2', sequence: 1)
          }
        end

        reviews_by_sequence = Booklog.reviews_by_sequence

        expect(reviews_by_sequence.first.isbn).to eq('isbn 1')
        expect(reviews_by_sequence.last.isbn).to eq('isbn 2')

        expect(Booklog.instance_variable_get('@reviews_by_sequence').length).to eq 2
      end
    end
  end

  describe '#authors' do
    it 'returns a collection of reviewed authors' do
      expect(Booklog).to(receive(:books)) do
        {
          'isbn 1' => OpenStruct.new(
            isbn: 'isbn 1',
            authors: [
              OpenStruct.new(slug: 'stephen-king'),
              OpenStruct.new(slug: 'peter-straub')
            ]
          ),
          'isbn 2' => OpenStruct.new(
            isbn: 'isbn 2',
            authors: [
              OpenStruct.new(slug: 'piers-anthony')
            ]
          ),
          'isbn 3' => OpenStruct.new(
            isbn: 'isbn 3',
            authors: [
              OpenStruct.new(slug: 'richard-laymon')
            ]
          ),
          'isbn 4' => OpenStruct.new(
            isbn: 'isbn 4',
            authors: [
              OpenStruct.new(slug: 'stephen-king')
            ]
          )
        }
      end

      expect(Booklog).to(receive(:reviews)) do
        {
          'isbn 1' => OpenStruct.new(isbn: 'isbn 1'),
          'isbn 3' => OpenStruct.new(isbn: 'isbn 3'),
          'isbn 4' => OpenStruct.new(isbn: 'isbn 3')
        }
      end

      authors = Booklog.authors
      expect(authors.length).to eq 3

      expect(authors.map(&:slug)).to match_array(
        ['stephen-king', 'richard-laymon', 'peter-straub']
      )
    end
  end

  describe '#readings_for_isbn' do
    it 'returns a collection of readings for the given isbn' do
      expect(Booklog).to(receive(:readings)) do
        [
          OpenStruct.new(isbn: 'isbn 1'),
          OpenStruct.new(isbn: 'isbn 2'),
          OpenStruct.new(isbn: 'isbn 3'),
          OpenStruct.new(isbn: 'isbn 2'),
        ]
      end

      readings = Booklog.readings_for_isbn(isbn: 'isbn 2')
      expect(readings.length).to eq 2
    end
  end
end
