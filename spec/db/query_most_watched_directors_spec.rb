# frozen_string_literal: true
require 'spec_helper'

describe Movielog::Db::QueryMostWatchedDirectors do
  let(:db) do
    titles = {
      'Rio Bravo (1959)' => {
        title: 'Rio Bravo (1959)',
        display_title: 'Rio Bravo (1959)',
        year: '1959',
        sortable_title: 'Rio Bravo (1959)',
        aka_titles: ["Howard Hawks' Rio Bravo"]
      },
      'Fright Night (1985)' => {
        title: 'Fright Night (1985)',
        display_title: 'Fright Night (1985)',
        year: '1985',
        sortable_title: 'Fright Night (1985)',
        aka_titles: []
      },
      "Child's Play (1988)" => {
        title: "Child's Play (1988)",
        display_title: "Child's Play (1988)",
        year: '1988',
        sortable_title: "Child's Play (1988)",
        aka_titles: []
      },
      'Thinner (1996)' => {
        title: 'Thinner (1996)',
        display_title: 'Thinner (1996)',
        year: '1996',
        sortable_title: 'Thinner (1996)',
        aka_titles: []
      }
    }

    viewings = {
      1 => OpenStruct.new(title: 'Rio Bravo (1959)', date: Date.parse('2011-03-12')),
      2 => OpenStruct.new(title: 'Fright Night (1985)', date: Date.parse('2012-03-12')),
      3 => OpenStruct.new(title: "Child's Play (1988)", date: Date.parse('2012-03-12')),
      4 => OpenStruct.new(title: 'Thinner (1996)', date: Date.parse('2013-03-12')),
      5 => OpenStruct.new(title: 'Fright Night (1985)', date: Date.parse('2013-03-12')),
      6 => OpenStruct.new(title: 'Fright Night (1985)', date: Date.parse('2014-03-12')),
      7 => OpenStruct.new(title: 'Fright Night (1985)', date: Date.parse('2015-03-12'))
    }

    cast_and_crew = {
      'Hawks, Howard' => {
        full_name: 'Hawks, Howard',
        last_name: 'Hawks',
        first_name: 'Howard',
        annotation: nil,
        director_credits: [
          { title: 'Rio Bravo (1959)',
            notes: nil }
        ]
      },
      'Holland, Tom' => {
        full_name: 'Holland, Tom',
        last_name: 'Holland',
        first_name: 'Tom',
        annotation: nil,
        director_credits: [
          {
            title: 'Fright Night (1985)',
            notes: nil
          },
          {
            title: "Child's Play (1988)",
            notes: nil
          }
        ]
      }
    }

    db = stub_movie_db(titles: titles, cast_and_crew: cast_and_crew)
    Movielog::Db::UpdateMostWatchedTables.call(db: db, viewings: viewings)
    db
  end

  it 'creates the most watched tables and populates the viewing list' do
    persons = Movielog::Db::QueryMostWatchedDirectors.call(db: db)

    expect(persons.length).to eq(1)
    expect(persons.first.full_name).to eq('Holland, Tom')
  end
end
