# frozen_string_literal: true
require 'spec_helper'

describe Movielog::Db::QueryMostReviewedPersons do
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

    db = stub_movie_db(titles: titles, cast_and_crew: cast_and_crew)
    Movielog::Db::UpdateMostReviewedTables.call(db: db, reviews: reviews)
    db
  end

  it 'creates the most watched tables and populates the viewing list' do
    persons = Movielog::Db::QueryMostReviewedPersons.call(db: db)

    expect(persons.length).to eq(2)
    expect(persons.keys.first).to eq('Dickinson, Angie')
    expect(persons.keys.last).to eq('Martin, Dean')
  end
end
