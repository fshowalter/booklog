# frozen_string_literal: true
require 'spec_helper'

describe Booklog::CreateReading do
  let(:book) do
    OpenStruct.new(id: 'the-test-book-by-test-author')
  end

  it('creates reading') do
    allow(File).to receive(:open).with('test-readings-path' + '/0012-the-test-book-by-test-author.yml', 'w')

    expect(Booklog::CreateReading.call(
      readings_path: 'test-readings-path',
      sequence: 12,
      book: book,
      isbn: '9876543210',
      pages_total: 256,
      pages_read: 256,
      date_started: '2011-11-04',
      date_finished: '2011-11-06',
    ).to_h).to eq(
      sequence: 12,
      book_id: 'the-test-book-by-test-author',
      isbn: '9876543210',
      pages_total: 256,
      pages_read: 256,
      date_started: '2011-11-04',
      date_finished: '2011-11-06',
    )
  end
end
