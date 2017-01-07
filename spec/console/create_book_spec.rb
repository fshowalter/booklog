# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreateBook do
  before(:each) do
    IOHelper.clear
  end

  let(:author1) do
    OpenStruct.new(id: 'author-1-id', name: 'Author 1', sortable_name: 'Author 1')
  end

  let(:author2) do
    OpenStruct.new(id: 'author-2-id', name: 'Author 2', sortable_name: 'Author 2')
  end

  let(:author3) do
    OpenStruct.new(id: 'author-3-id', name: 'Author 3', sortable_name: 'Author 3')
  end

  let(:authors) do
    {
      'author-2-id' => author2,
      'author-1-id' => author1,
      'author-3-id' => author3,
    }
  end

  it 'calls Booklog::CreateBook with correct data' do
    IOHelper.type_input('Book to Test')
    IOHelper.confirm
    IOHelper.select
    IOHelper.confirm
    IOHelper.confirm
    IOHelper.type_input('Alternate Title')
    IOHelper.confirm
    IOHelper.select
    IOHelper.type_input('Author')
    IOHelper.move_down
    IOHelper.select
    IOHelper.confirm
    IOHelper.type_input('Author')
    IOHelper.move_down
    IOHelper.move_down
    IOHelper.select
    IOHelper.select
    IOHelper.type_input('1234567890')
    IOHelper.confirm
    IOHelper.type_input('1976')
    IOHelper.confirm

    expect(Booklog::Console::CreateBook).to receive(:puts).twice

    expect(Booklog::CreateBook).to receive(:call).with(
      title: 'Book to Test',
      sortable_title: 'Book to Test',
      aka_titles: [
        'Alternate Title',
      ],
      authors: [
        author2,
        author3,
      ],
      isbn: '1234567890',
      year_published: '1976',
    ).and_return(OpenStruct.new(id: 'new-book-id'))

    Booklog::Console::CreateBook.call(authors: authors)
  end

  describe 'when book starts with "The"' do
    it 'calls Booklog::CreateBook with correct sortable title' do
      IOHelper.type_input('The Book to Test')
      IOHelper.confirm
      IOHelper.select
      IOHelper.confirm
      IOHelper.select
      IOHelper.type_input('Author')
      IOHelper.select
      IOHelper.select
      IOHelper.type_input('1234567890')
      IOHelper.confirm
      IOHelper.type_input('1976')
      IOHelper.confirm

      expect(Booklog::Console::CreateBook).to receive(:puts).twice

      expect(Booklog::CreateBook).to receive(:call).with(
        title: 'The Book to Test',
        sortable_title: 'Book to Test, The',
        aka_titles: [],
        authors: [
          author1,
        ],
        isbn: '1234567890',
        year_published: '1976',
      ).and_return(OpenStruct.new(id: 'new-book-id'))

      Booklog::Console::CreateBook.call(authors: authors)
    end
  end
end
