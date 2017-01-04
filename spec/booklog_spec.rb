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

  describe '#next_reading_number' do
    it 'returns the number of readings plus one' do
      expect(Booklog::ParseReadings).to(
        receive(:call).with(readings_path: Booklog.readings_path)
      ) do
        {
          1 => OpenStruct.new(db_title: 'title 1', sequence: 2),
          2 => OpenStruct.new(db_title: 'title 2', sequence: 1)
        }
      end

      expect(Booklog.next_reading_number).to eq 3
    end
  end

  describe '#reviews_by_sequence' do
    it 'returns the reviews sorted by sequence in reverse' do
      expect(Booklog::ParseReviews).to(
        receive(:call).with(reviews_path: Booklog.reviews_path)
      ) do
        {
          'title 1' => OpenStruct.new(db_title: 'title 1', sequence: 2),
          'title 2' => OpenStruct.new(db_title: 'title 2', sequence: 1)
        }
      end

      reviews_by_sequence = Booklog.reviews_by_sequence

      expect(reviews_by_sequence.first.db_title).to eq('title 1')
      expect(reviews_by_sequence.last.db_title).to eq('title 2')
    end
  end

  describe '#readings_for_book_id' do
    it 'returns a collection of readings for the given book_id' do
      expect(Booklog).to(receive(:readings)) do
        [
          OpenStruct.new(book_id: 'the-shining-by-stephen-king', sequence: 1),
          OpenStruct.new(book_id: 'night-shift-by-stephen-king', sequence: 2),
          OpenStruct.new(book_id: 'the-shining-by-stephen-king', sequence: 3)
        ]
      end

      readings = Booklog.readings_for_book_id(book_id: 'the-shining-by-stephen-king')
      expect(readings.length).to eq 2
      expect(readings.first.book_id).to eq 'the-shining-by-stephen-king'
      expect(readings.first.sequence).to eq 1
      expect(readings.last.book_id).to eq 'the-shining-by-stephen-king'
      expect(readings.last.sequence).to eq 3
    end
  end
end
