# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreateReading do
  let(:book1) do
    OpenStruct.new(id: 'book-1-id', title: 'Book 1', sortable_title: 'Book 1')
  end

  let(:book2) do
    OpenStruct.new(id: 'book-2-id', title: 'Book 2', sortable_title: 'Book 2')
  end

  let(:book3) do
    OpenStruct.new(id: 'book-3-id', title: 'Book 3', sortable_title: 'Book 3')
  end

  let(:books) do
    {
      'book-2-id' => book2,
      'book-1-id' => book1,
      'book-3-id' => book3,
    }
  end

  before(:each) do
    IOHelper.clear
  end

  it 'calls Booklog::CreateReading with correct data' do
    IOHelper.type_input('Book')
    IOHelper.move_down
    IOHelper.select
    IOHelper.type_input('9876543210')
    IOHelper.confirm
    IOHelper.type_input('276')
    IOHelper.confirm
    IOHelper.type_input('2011-11-04')
    IOHelper.confirm
    IOHelper.type_input('2011-11-06')
    IOHelper.confirm

    expect(Booklog::Console::CreateReading).to receive(:puts).twice

    expect(Booklog::CreateReading).to receive(:call).with(
      book: book2,
      isbn: '9876543210',
      pages_read: '276',
      pages_total: '276',
      date_started: Date.parse('2011-11-04'),
      date_finished: Date.parse('2011-11-06'),
    ).and_return(OpenStruct.new(sequence: 'new-sequence-number'))

    Booklog::Console::CreateReading.call(books: books)
  end
end
