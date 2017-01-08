# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Booklog::ParseBooks do
  let(:author) do
    OpenStruct.new
  end

  let(:authors) do
    {
      'stephen-king' => author,
    }
  end

  let(:files) do
    {
      'book1.yml' => <<-EOF,
---
:id: the-shining-by-stephen-king
:title: The Shining
:sortable_title: Shining, The
:aka_titles: []
:author_ids:
- stephen-king
:isbn: '9780385121675'
:year_published: '1977'
      EOF

      'book2.yml' => <<-EOF
---
:id: night-shift-by-stephen-king
:title: Night Shift
:sortable_title: Night Shift
:aka_titles: []
:author_ids:
- stephen-king
:isbn: '9780385129916'
:year_published: '1978'
      EOF
    }
  end

  it 'reads books from the given directory' do
    stub_files(files: files, path: 'test_books_path/*.yml')

    books = Booklog::ParseBooks.call(books_path: 'test_books_path', authors: authors)

    expect(books.keys).to eq([
                               'the-shining-by-stephen-king',
                               'night-shift-by-stephen-king',
                             ])
  end

  context 'when error parsing yaml' do
    let(:bad_files) do
      {
        'book1.yml' => <<-EOF,
---
:id: 1
1:bad
---
        EOF
      }
    end

    it 'writes an error message' do
      stub_files(files: bad_files, path: 'test_books_path/*.yml')

      expect(Booklog::ParseBooks).to receive(:puts) do |arg|
        expect(arg).to start_with('YAML Exception reading book1.yml:')
      end

      Booklog::ParseBooks.call(books_path: 'test_books_path', authors: authors)
    end
  end

  context 'when error book file' do
    let(:bad_file) do
      {
        'book1.yml' => <<-EOF,
---
:bad_file: true
---
      EOF

        'book2.yml' => <<-EOF
---
:id: night-shift-by-stephen-king
:title: Night Shift
:sortable_title: Night Shift
:aka_titles: []
:author_ids:
- stephen-king
:isbn: '9780385129916'
:year_published: '1978'
      EOF
      }
    end
    it 'writes an error message' do
      stub_files(files: bad_file, path: 'test_books_path/*.yml')

      original_load = YAML.method(:load)
      expect(YAML).to receive(:load).with("---\n:bad_file: true\n---\n").and_raise(RuntimeError)
      expect(YAML).to receive(:load) do |args|
        original_load.call(args)
      end

      expect(Booklog::ParseBooks).to receive(:puts)
        .with('Error reading book1.yml: RuntimeError')

      Booklog::ParseBooks.call(books_path: 'test_books_path', authors: authors)
    end
  end
end
