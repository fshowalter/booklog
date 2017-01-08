# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Booklog::ParseReviews do
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

  let(:files) do
    {
      'review1.md' => <<-EOF,
---
:sequence: 1
:book_id: book-2-id
:date: 2016-12-30
:grade: B+
:cover: cover
:cover_placeholder: placeholder
---
Review 1 content.
      EOF

      'review2.md' => <<-EOF
---
:sequence: 2
:book_id: book-3-id
:date: 2017-01-02
:grade: C+
:cover: cover
:cover_placeholder: placeholder
---
Review 2 content.
      EOF
    }
  end

  it 'reads reviews from the given directory' do
    stub_files(files: files, path: 'test_reviews_path/*.md')

    reviews = Booklog::ParseReviews.call(reviews_path: 'test_reviews_path', books: books)

    expect(reviews.keys).to eq ['book-2-id', 'book-3-id']

    expect(reviews['book-2-id'].title).to eq 'Book 2'
    expect(reviews['book-2-id'].content).to eq "Review 1 content.\n"
    expect(reviews['book-3-id'].title).to eq 'Book 3'
    expect(reviews['book-3-id'].content).to eq "Review 2 content.\n"
  end

  context 'when error parsing yaml' do
    let(:bad_files) do
      {
        'review1.md' => <<-EOF,
---
:sequence: 1
1:bad
---
Review 1 content.
        EOF
      }
    end

    it 'writes an error message' do
      stub_files(files: bad_files, path: 'test_reviews_path/*.md')

      expect(Booklog::ParseReviews).to receive(:puts) do |arg|
        expect(arg).to start_with('YAML Exception reading review1.md:')
      end

      Booklog::ParseReviews.call(reviews_path: 'test_reviews_path', books: books)
    end
  end

  context 'when error reading file' do
    let(:bad_file) do
      {
        'review1.md' => <<-EOF,
---
:bad_file: true
---
Review 1 content.
      EOF

        'review2.md' => <<-EOF
---
:sequence: 2
:book_id: book-3-id
:date: 2017-01-02
:grade: C+
:cover: cover
:cover_placeholder: placeholder
---
Review 2 content.
      EOF
      }
    end
    it 'writes an error message' do
      stub_files(files: bad_file, path: 'test_reviews_path/*.md')

      original_load = YAML.method(:load)
      expect(YAML).to receive(:load).with("---\n:bad_file: true\n").and_raise(RuntimeError)
      expect(YAML).to receive(:load) do |args|
        original_load.call(args)
      end

      expect(Booklog::ParseReviews).to receive(:puts)
        .with('Error reading review1.md: RuntimeError')

      Booklog::ParseReviews.call(reviews_path: 'test_reviews_path', books: books)
    end
  end
end
