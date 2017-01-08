# frozen_string_literal: true
require 'spec_helper'

describe Booklog::CreateBook do
  let(:authors) do
    [
      OpenStruct.new(id: 'test-author', name: 'Test Author'),
    ]
  end

  it('creates book') do
    allow(File).to receive(:open).and_call_original
    allow(File).to receive(:open).with('test-books-path' + '/the-test-book-by-test-author.yml', 'w')

    expect(Booklog::CreateBook.call(
      books_path: 'test-books-path',
      title: 'The Test Book',
      sortable_title: 'Test Book, The',
      aka_titles: [],
      authors: authors,
      isbn: '9876543210',
      year_published: '1997',
    ).to_h).to eq(
      id: 'the-test-book-by-test-author',
      title: 'The Test Book',
      sortable_title: 'Test Book, The',
      aka_titles: [],
      author_ids: [
        'test-author',
      ],
      isbn: '9876543210',
      year_published: '1997',
    )
  end
end
