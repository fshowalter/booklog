# frozen_string_literal: true
require 'spec_helper'

describe Movielog::Db::QueryRelatedTitlesByCast do
  let(:db) do
    titles = {
      'Rio Bravo (1959)' => {
        title: 'Rio Bravo (1959)',
        display_title: 'Rio Bravo (1959)',
        year: '1959',
        sortable_title: 'Rio Bravo (1959)',
        aka_titles: ["Howard Hawks' Rio Bravo"]
      },
      "Ocean's 11 (1960)" => {
        title: "Ocean's 11 (1960)",
        display_title: "Ocean's 11 (1960)",
        year: '1960',
        sortable_title: "Ocean's 11 (1960)",
        aka_titles: []
      },
      'Some Came Running (1958)' => {
        title: 'Some Came Running (1958)',
        display_title: 'Some Came Running (1958)',
        year: '1958',
        sortable_title: 'Some Came Running (1958)',
        aka_titles: []
      },
      'Kiss Me, Stupid (1964)' => {
        title: 'Kiss Me, Stupid (1964)',
        display_title: 'Kiss Me, Stupid (1964)',
        year: '1964',
        sortable_title: 'Kiss Me, Stupid (1964)',
        aka_titles: []
      },
      'The Silencers (1966)' => {
        title: 'The Silencers (1966)',
        display_title: 'The Silencers (1966)',
        year: '1966',
        sortable_title: 'Silencers, The (1966)',
        aka_titles: []
      }
    }

    reviews = {
      '1' => OpenStruct.new(
        title: 'Rio Bravo (1959)',
        db_title: 'Rio Bravo (1959)',
        date: Date.parse('2011-03-12')
      ),
      '2' => OpenStruct.new(
        title: "Ocean's 11 (1960)",
        db_title: "Ocean's 11 (1960)",
        date: Date.parse('2011-06-11')
      ),
      '3' => OpenStruct.new(
        title: 'Some Came Running (1958)',
        db_title: 'Some Came Running (1958)',
        date: Date.parse('2012-01-11')
      ),
      '4' => OpenStruct.new(
        title: 'Kiss Me, Stupid (1964)',
        db_title: 'Kiss Me, Stupid (1964)',
        date: Date.parse('2013-02-22')
      ),
      '5' => OpenStruct.new(
        title: 'The Silencers (1966)',
        db_title: 'The Silencers (1966)',
        date: Date.parse('2014-04-14')
      )
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
            position_in_credits: '4' },
          { title: "Ocean's 11 (1960)",
            notes: nil,
            role: 'Beatrice Ocean',
            position_in_credits: '5' }
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
            position_in_credits: '2' },
          { title: "Ocean's 11 (1960)",
            notes: nil,
            role: 'Sam Harmon',
            position_in_credits: '2' },
          {
            title: 'Some Came Running (1958)',
            notes: nil,
            role: 'Bama Dillert',
            position_in_credits: '2'
          },
          {
            title: 'Kiss Me, Stupid (1964)',
            notes: nil,
            role: 'Dino',
            position_in_credits: '1'
          },
          {
            title: 'The Silencers (1966)',
            notes: nil,
            role: 'Matt Helm',
            position_in_credits: '1'
          }
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

    db = stub_movie_db(titles: titles, cast_and_crew: cast_and_crew)
    Movielog::Db::UpdateMostReviewedTables.call(db: db, reviews: reviews)
    db
  end

  it 'finds related titles for cast' do
    persons = Movielog::Db::QueryRelatedTitlesByCast.call(db: db, title: 'Rio Bravo (1959)')

    expect(persons.length).to eq(1)
    expect(persons.keys.first.full_name).to eq('Martin, Dean')
  end
end
