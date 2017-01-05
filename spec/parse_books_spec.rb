# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Booklog::ParseBooks do
  let(:files) do
    {
      'book1.yml' => <<-EOF,
---
:title: The Shining
:aka_titles: []
:authors:
- King, Stephen
:page_count: '447'
:year_published: '1977'
:isbn: '1234567890'
:cover: 'cover'
:cover_placeholder: 'placeholder'
---
      EOF

      'book2.yml' => <<-EOF
---
:title: Night Shift
:aka_titles: []
:authors:
- King, Stephen
:page_count: '326'
:year_published: '1978'
:isbn: '0987654321'
:cover: 'cover'
:cover_placeholder: 'placeholder'

---
      EOF
    }
  end

  it 'reads books from the given directory' do
    stub_files(files: files, path: 'test_books_path/*.yml')

    books = Booklog::ParseBooks.call(books_path: 'test_books_path')

    expect(books.length).to eq 2

    expect(books['1234567890'].isbn).to eq '1234567890'
    expect(books['0987654321'].isbn).to eq '0987654321'
  end

  context 'when error parsing yaml' do
    let(:bad_files) do
      {
        'book1.yml' => <<-EOF,
---
:sequence: 1
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

      Booklog::ParseBooks.call(books_path: 'test_books_path')
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
:title: Night Shift
:aka_titles: []
:authors:
- King, Stephen
:page_count: '326'
:year_published: '1978'
:isbn: '0987654321'
:cover: 'cover'
:cover_placeholder: 'placeholder'
---
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

      Booklog::ParseBooks.call(books_path: 'test_books_path')
    end
  end
end
