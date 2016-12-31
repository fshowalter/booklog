# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Movielog::Console::CreateReview do
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

  before(:each) do
    IOHelper.clear
    allow(File).to receive(:open).with(Movielog.reviews_path + '/rio-bravo-1959.md', 'w')
    allow(Movielog).to receive(:db).and_return(db)
  end

  it 'creates review' do
    IOHelper.type_input('rio bravo')
    IOHelper.type_input("\r")

    expect(Movielog::Console::CreateReview).to(receive(:puts))
    expect(Movielog).to receive(:next_post_number).and_return(2)
    expect(Movielog).to receive(:viewed_titles) do
      [
        'Rio Bravo (1959)',
        'Reservoir Dogs (1992)',
        'The Big Sleep (1946)'
      ]
    end

    review = Movielog::Console::CreateReview.call
    expect(review.title).to eq 'Rio Bravo (1959)'
    expect(review.db_title).to eq 'Rio Bravo (1959)'
    expect(review.sequence).to eq 2
  end
end
