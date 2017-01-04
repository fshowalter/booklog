# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreateReading do
  let(:books) do
    {
      'the-shining-by-stephen-king' => OpenStruct.new(
        id: 'the-shining-by-stephen-king',
        title: 'The Shining',
        authors: [
          OpenStruct.new(name: 'Stephen King')
        ]
      )
    }
  end

  before(:each) do
    IOHelper.clear
    allow(File).to receive(:open).and_call_original
    allow(File).to receive(:open).with(Booklog.readings_path + '/0001-the-shining-by-stephen-king.yml', 'w')
    allow(Booklog).to receive(:reviews).and_return({})

    expect(Booklog).to receive(:books).and_return(books)
    expect(Booklog).to receive(:next_reading_number).and_return(12)
  end

  it 'creates reading' do
    IOHelper.type_input('The Shining')
    IOHelper.select
    IOHelper.type_input('447')
    IOHelper.confirm
    IOHelper.type_input('2011-11-04')
    IOHelper.confirm
    IOHelper.type_input('2011-11-06')
    IOHelper.confirm

    expect(Booklog::Console::CreateReading).to receive(:puts)

    reading = Booklog::Console::CreateReading.call

    expect(reading.to_h).to eq(
      book_id: 'the-shining-by-stephen-king',
      pages_read: '447',
      sequence: 12,
      date_started: Date.parse('2011-11-04'),
      date_finished: Date.parse('2011-11-06')
    )
  end
end
