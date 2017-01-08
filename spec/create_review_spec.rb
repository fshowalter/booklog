# frozen_string_literal: true
require 'spec_helper'

describe Booklog::CreateReview do
  let(:book) do
    OpenStruct.new(id: 'the-test-book-by-test-author')
  end

  it('creates review') do
    allow(File).to receive(:open).with('test-reviews-path' + '/0012-the-test-book-by-test-author.md', 'w')

    expect(Booklog::CreateReview.call(
      reviews_path: 'test-reviews-path',
      sequence: 12,
      book: book,
    ).to_h).to eq(
      sequence: 12,
      book_id: 'the-test-book-by-test-author',
      date: Date.today,
      grade: '',
      cover: '',
      cover_placeholder: nil,
    )
  end
end
