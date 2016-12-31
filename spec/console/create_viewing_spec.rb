# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Movielog::Console::CreateViewing do
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
    allow(File).to receive(:open).with(Movielog.viewings_path + '/0012-rio-bravo-1959.yml', 'w')
    allow(Movielog).to receive(:db).and_return(db)
  end

  it 'creates viewing' do
    IOHelper.type_input('rio bravo')
    IOHelper.select
    IOHelper.type_input('2014-08-30')
    IOHelper.confirm
    IOHelper.move_down
    IOHelper.select
    IOHelper.type_input('Blu-ray')
    IOHelper.confirm

    expect(Movielog::Console::CreateViewing).to receive(:puts)
    expect(Movielog).to receive(:next_viewing_number).and_return(12)
    expect(Movielog).to receive(:venues) do
      [
        'Nextflix'
      ]
    end

    viewing = Movielog::Console::CreateViewing.call
    expect(viewing.to_h).to eq(

      title: 'Rio Bravo (1959)',
      db_title: 'Rio Bravo (1959)',
      number: 12,
      venue: 'Blu-ray',
      date: Date.parse('2014-8-30')
    )
  end
end
