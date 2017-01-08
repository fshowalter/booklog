# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreateReview do
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

  it 'calls Booklog::CreateReview with correct data' do
    IOHelper.type_input('Book')
    IOHelper.move_down
    IOHelper.select

    expect(Booklog::Console::CreateReview).to receive(:puts).twice

    expect(Booklog::CreateReview).to receive(:call).with(
      book: book2,
    ).and_return(OpenStruct.new(sequence: 'new-sequence-number'))

    Booklog::Console::CreateReview.call(books: books)
  end
end
