# frozen_string_literal: true
require 'spec_helper'

describe Movielog::Db::UpdateMostWatchedTables do
  let(:db) do
    titles = {
      'Rio Bravo (1959)' => {
        title: 'Rio Bravo (1959)',
        display_title: 'Rio Bravo (1959)',
        year: '1959',
        sortable_title: 'Rio Bravo (1959)',
        aka_titles: ["Howard Hawks' Rio Bravo"]
      }
    }

    cast_and_crew = {
      'Dickinson, Angie' => {
        full_name: 'Dickinson, Angie',
        last_name: 'Dickinson',
        first_name: 'Angie',
        annotation: nil,
        performer_credits: [
          { title: 'Rio Bravo (1959)',
            notes: nil,
            role: 'Feathers',
            position_in_credits: '4' }
        ]
      },
      'Martin, Dean' => {
        full_name: 'Martin, Dean',
        last_name: 'Martin',
        first_name: 'Dean',
        annotation: nil,
        performer_credits: [
          { title: 'Rio Bravo (1959)',
            notes: nil,
            role: "Dude ('Borachón')",
            position_in_credits: '2' }
        ]
      },
      'Wayne, John' => {
        full_name: 'Wayne, John',
        last_name: 'Wayne',
        first_name: 'John',
        annotation: nil,
        performer_credits: [
          { title: 'Rio Bravo (1959)',
            notes: nil,
            role: 'Sheriff John T. Chance',
            position_in_credits: '1' }
        ]
      },
      'Nelson, Ricky' => {
        full_name: 'Nelson, Ricky',
        last_name: 'Nelson',
        first_name: 'Ricky',
        annotation: nil,
        performer_credits: [
          { title: 'Rio Bravo (1959)',
            notes: nil,
            role: 'Colorado Ryan',
            position_in_credits: '3' }
        ]
      }
    }

    stub_movie_db(titles: titles, cast_and_crew: cast_and_crew)
  end

  let(:viewings) do
    {
      1 => OpenStruct.new(title: 'Rio Bravo (1959)', date: Date.parse('2011-03-12'))
    }
  end

  it 'creates the most watched tables and populates the viewing list' do
    Movielog::Db::UpdateMostWatchedTables.call(db: db, viewings: viewings)

    viewings_info = [
      {
        'cid' => 0,
        'name' => 'id',
        'type' => 'INTEGER',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 1
      },
      {
        'cid' => 1,
        'name' => 'title',
        'type' => 'varchar(255)',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      },
      {
        'cid' => 2,
        'name' => 'date',
        'type' => 'date',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      }
    ]

    most_watched_info = [
      {
        'cid' => 0,
        'name' => 'id',
        'type' => 'INTEGER',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 1
      },
      {
        'cid' => 1,
        'name' => 'full_name',
        'type' => 'varchar(255)',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      },
      {
        'cid' => 2,
        'name' => 'movie_count',
        'type' => 'INTEGER',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      },
      {
        'cid' => 3,
        'name' => 'watched_movie_count',
        'type' => 'INTEGER',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      },
      {
        'cid' => 4,
        'name' => 'percent_seen',
        'type' => 'FLOAT',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      },
      {
        'cid' => 5,
        'name' => 'watch_count',
        'type' => 'INTEGER',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      },
      {
        'cid' => 6,
        'name' => 'most_recent_watch_date',
        'type' => 'DATE',
        'notnull' => 1,
        'dflt_value' => nil,
        'pk' => 0
      }
    ]

    expect(db.table_info('viewings')).to eq viewings_info
    expect(db.table_info('most_watched_performers')).to eq most_watched_info
    expect(db.table_info('most_watched_directors')).to eq most_watched_info
    expect(db.table_info('most_watched_writers')).to eq most_watched_info
  end
end
