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
      expect(Booklog.site_tagline).to eq 'Literature is a Relative Term'
    end
  end

  describe '#next_reading_sequence' do
    it 'returns the length of readings plus one' do
      readings = {
        1 => OpenStruct.new(sequence: 3),
        2 => OpenStruct.new(sequence: 1),
      }

      expect(Booklog.next_reading_sequence(readings: readings)).to eq 3
    end
  end

  describe '#next_review_sequence' do
    it 'returns the length of reviews plus one' do
      reviews = {
        1 => OpenStruct.new(sequence: 3),
        2 => OpenStruct.new(sequence: 1),
      }

      expect(Booklog.next_review_sequence(reviews: reviews)).to eq 3
    end
  end

  describe '#books' do
    it 'calls Booklog::ParseBooks' do
      expect(Booklog::ParseBooks).to(receive(:call)).and_return('parse data')

      expect(Booklog.books(authors: {})).to eq 'parse data'
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

      expect(Booklog.reviews(books: {})).to eq 'parse data'
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

        expect(Booklog.reviews(books: {})).to eq 'parse data'

        expect(Booklog.instance_variable_get('@reviews')).to eq 'parse data'
      end
    end
  end

  describe '#reviews_by_author' do
    let(:author1) do
      OpenStruct.new(name: 'Author 1')
    end

    let(:author2) do
      OpenStruct.new(name: 'Author 2')
    end

    let(:author3) do
      OpenStruct.new(name: 'Author 3')
    end

    let(:review1) do
      OpenStruct.new(id: 'review-1', authors: [author1])
    end

    let(:review2) do
      OpenStruct.new(id: 'review-2', authors: [author1, author2])
    end

    let(:review3) do
      OpenStruct.new(id: 'review-3', authors: [author3])
    end

    let(:reviews) do
      {
        'review-1' => review1,
        'review-2' => review2,
        'review-3' => review3,
      }
    end

    it 'rehashes reviews by author' do
      reviews_by_author = Booklog.reviews_by_author(reviews: reviews)

      expect(reviews_by_author).to match(author1 => [review1, review2],
                                         author2 => [review2],
                                         author3 => [review3])
    end

    describe 'when #cache_reviews is true' do
      before(:each) do
        Booklog.cache_reviews = true
      end

      after(:each) do
        Booklog.cache_reviews = false
      end

      it 'rehashes reviews by author' do
        Booklog.reviews_by_author(reviews: reviews)

        expect(Booklog.instance_variable_get('@reviews_by_author')).to match(author1 => [review1, review2],
                                                                             author2 => [review2],
                                                                             author3 => [review3])
      end
    end
  end

  describe '#readings' do
    it 'calls Booklog::ParseReadings' do
      expect(Booklog::ParseReadings).to(receive(:call)).and_return('parse data')

      expect(Booklog.readings(books: {})).to eq 'parse data'
    end
  end

  describe '#reviews_by_sequence' do
    it 'returns the reviews sorted by sequence in reverse' do
      reviews = {
        'book-id-1' => OpenStruct.new(sequence: 1),
        'book-id-2' => OpenStruct.new(sequence: 2),
      }

      reviews_by_sequence = Booklog.reviews_by_sequence(reviews: reviews)

      expect(reviews_by_sequence.first.sequence).to eq(2)
      expect(reviews_by_sequence.last.sequence).to eq(1)
    end

    describe 'when #cache_reviews is true' do
      before(:each) do
        Booklog.cache_reviews = true
      end

      after(:each) do
        Booklog.cache_reviews = false
      end

      it 'caches reviews_by_sequence' do
        reviews = {
          'book-id-1' => OpenStruct.new(sequence: 1),
          'book-id-2' => OpenStruct.new(sequence: 2),
        }

        reviews_by_sequence = Booklog.reviews_by_sequence(reviews: reviews)

        expect(reviews_by_sequence.first.sequence).to eq(2)
        expect(reviews_by_sequence.last.sequence).to eq(1)

        expect(Booklog.instance_variable_get('@reviews_by_sequence').length).to eq 2
      end
    end
  end

  describe '#authors' do
    it 'calls Booklog::ParseAuthors' do
      expect(Booklog::ParseAuthors).to(receive(:call)).and_return('parse data')

      expect(Booklog.authors).to eq 'parse data'
    end
  end

  describe '#readings_for_book_id' do
    it 'returns a collection of readings for the given book_id' do
      readings = [
        OpenStruct.new(book_id: 'book-1'),
        OpenStruct.new(book_id: 'book-2'),
        OpenStruct.new(book_id: 'book-3'),
        OpenStruct.new(book_id: 'book-2'),
      ]

      readings = Booklog.readings_for_book_id(readings: readings, book_id: 'book-2')
      expect(readings.length).to eq 2
    end
  end
end
