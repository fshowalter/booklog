# frozen_string_literal: true
require 'spec_helper'

describe Movielog do
  before(:each) do
    allow(MovieDb).to receive(:info_for_title) do
      OpenStruct.new(
        sortable_title: 'stubbed title',
        release_date: 'stubbed release date'
      )
    end
  end

  describe '#site_url' do
    it 'returns the site url' do
      expect(Movielog.site_url).to eq 'https://www.franksmovielog.com'
    end
  end

  describe '#site_title' do
    it 'returns the site title' do
      expect(Movielog.site_title).to eq "Frank's Movie Log"
    end
  end

  describe '#next_viewing_number' do
    it 'returns the number of viewings plus one' do
      expect(Movielog::ParseViewings).to(
        receive(:call).with(viewings_path: Movielog.viewings_path)
      ) do
        {
          1 => OpenStruct.new(db_title: 'title 1', sequence: 2),
          2 => OpenStruct.new(db_title: 'title 2', sequence: 1)
        }
      end

      expect(Movielog.next_viewing_number).to eq 3
    end
  end

  describe '#reviews_by_sequence' do
    it 'returns the reviews sorted by sequence in reverse' do
      expect(Movielog::ParseReviews).to(
        receive(:call).with(reviews_path: Movielog.reviews_path)
      ) do
        {
          'title 1' => OpenStruct.new(db_title: 'title 1', sequence: 2),
          'title 2' => OpenStruct.new(db_title: 'title 2', sequence: 1)
        }
      end

      reviews_by_sequence = Movielog.reviews_by_sequence

      expect(reviews_by_sequence.first.db_title).to eq('title 1')
      expect(reviews_by_sequence.last.db_title).to eq('title 2')
    end
  end

  describe '#next_post_number' do
    it 'returns the number of reviews and features plus one' do
      expect(Movielog::ParseReviews).to(
        receive(:call).with(reviews_path: Movielog.reviews_path)
      ) do
        {
          'title 1' => OpenStruct.new(db_title: 'title 1', sequence: 2),
          'title 2' => OpenStruct.new(db_title: 'title 2', sequence: 1)
        }
      end

      expect(Movielog::ParsePages).to(
        receive(:call).with(pages_path: Movielog.pages_path)
      ) do
        {
          2 => 'a page'
        }
      end

      expect(Movielog.next_post_number).to eq 4
    end
  end

  describe '#db' do
    it 'returns a new movie_db instance' do
      expect(Movielog.db).to be_an_instance_of(SQLite3::Database)
    end
  end

  describe '#cast_and_crew' do
    it 'calls Movielog::Db::QueryMostReviewedPersons' do
      expect(Movielog::Db::QueryMostReviewedPersons).to receive(:call)

      Movielog.cast_and_crew
    end
  end

  describe '#viewed_titles' do
    it 'returns a unique collection of viewed titles' do
      expect(Movielog).to(receive(:viewings)) do
        {
          1 => OpenStruct.new(db_title: 'Rio Bravo (1959)'),
          2 => OpenStruct.new(db_title: 'The Big Sleep (1946)'),
          3 => OpenStruct.new(db_title: 'Reservoir Dogs (1992)'),
          4 => OpenStruct.new(db_title: 'North by Northwest (1959)'),
          5 => OpenStruct.new(db_title: 'Rio Bravo (1959)'),
          6 => OpenStruct.new(db_title: 'Some Like it Hot (1959)')
        }
      end

      expect(Movielog.viewed_titles).to match_array([
                                                      'Rio Bravo (1959)',
                                                      'The Big Sleep (1946)',
                                                      'Reservoir Dogs (1992)',
                                                      'North by Northwest (1959)',
                                                      'Some Like it Hot (1959)'
                                                    ])
    end
  end

  describe '#venues' do
    it 'returns a unique collection of venues' do
      expect(Movielog::ParseViewings).to(
        receive(:call).with(viewings_path: Movielog.viewings_path)
      ) do
        {
          1 => OpenStruct.new(venue: 'Blu-ray'),
          2 => OpenStruct.new(venue: 'Amazon Instant'),
          3 => OpenStruct.new(venue: 'DVD'),
          4 => OpenStruct.new(venue: 'Blu-ray'),
          5 => OpenStruct.new(venue: 'Netflix Streaming')
        }
      end

      expect(Movielog.venues).to eq([
                                      'Amazon Instant',
                                      'Blu-ray',
                                      'DVD',
                                      'Netflix Streaming'
                                    ])
    end
  end

  describe '#viewings_for_title' do
    it 'returns a collection of viewings for the given title' do
      expect(Movielog::ParseViewings).to(
        receive(:call).with(viewings_path: Movielog.viewings_path)
      ) do
        {
          1 => OpenStruct.new(db_title: 'Rio Bravo (1959)', sequence: 1),
          2 => OpenStruct.new(db_title: 'The Big Sleep (1946)', sequence: 2),
          3 => OpenStruct.new(db_title: 'Reservoir Dogs (1992)', sequence: 3),
          4 => OpenStruct.new(db_title: 'North by Northwest (1959)', sequence: 4),
          5 => OpenStruct.new(db_title: 'Rio Bravo (1959)', sequence: 5),
          6 => OpenStruct.new(db_title: 'Some Like it Hot (1959)', sequence: 6)
        }
      end

      viewings = Movielog.viewings_for_title(title: 'Rio Bravo (1959)')
      expect(viewings.length).to eq 2
      expect(viewings.first.db_title).to eq 'Rio Bravo (1959)'
      expect(viewings.first.sequence).to eq 1
      expect(viewings.last.db_title).to eq 'Rio Bravo (1959)'
      expect(viewings.last.sequence).to eq 5
    end
  end
end
