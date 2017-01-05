# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreateBook do
  before(:each) do
    IOHelper.clear
    allow(File).to receive(:open).and_call_original
    allow(File).to receive(:open).with(Booklog.books_path + '/test-book-by-joe-user.yml', 'w')
  end

  it 'creates book' do
    IOHelper.type_input('Test Book')
    IOHelper.confirm
    IOHelper.confirm
    IOHelper.type_input('Alternate Title')
    IOHelper.confirm
    IOHelper.select
    IOHelper.type_input('User, Joe')
    IOHelper.confirm
    IOHelper.select
    IOHelper.type_input('123')
    IOHelper.confirm
    IOHelper.type_input('1976')
    IOHelper.confirm
    IOHelper.type_input('1234567890')
    IOHelper.confirm

    expect(Booklog::Console::CreateBook).to receive(:puts)

    book = Booklog::Console::CreateBook.call

    expect(book.to_h).to eq(
      id: 'test-book-by-joe-user',
      title: 'Test Book',
      aka_titles: [
        'Alternate Title',
      ],
      page_count: '123',
      authors: [
        'User, Joe'
      ],
      year_published: '1976',
      isbn: '1234567890',
      cover: '',
      cover_placeholder: nil
    )
  end
end
