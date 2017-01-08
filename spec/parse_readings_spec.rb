# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Booklog::ParseReadings do
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
      'reading1.yml' => <<-EOF,
---
:sequence: 1
:book_id: book-2-id
:isbn: '0451150325'
:pages_total: '447'
:pages_read: '447'
:date_started: 2011-11-04
:date_finished: 2011-11-06
      EOF

      'reading2.yml' => <<-EOF
---
:sequence: 2
:book_id: book-3-id
:isbn: '9780451150707'
:pages_total: '326'
:pages_read: '326'
:date_started: 2012-05-13
:date_finished: 2012-05-14
      EOF
    }
  end

  it 'reads readings from the given directory' do
    stub_files(files: files, path: 'test_readings_path/*.yml')

    readings = Booklog::ParseReadings.call(readings_path: 'test_readings_path', books: books)

    expect(readings.length).to eq 2

    expect(readings.first.title).to eq 'Book 2'
    expect(readings.last.title).to eq 'Book 3'
  end

  context 'when error parsing yaml' do
    let(:bad_files) do
      {
        'reading1.yml' => <<-EOF,
---
:sequence: 1
1:bad
---
        EOF
      }
    end

    it 'writes an error message' do
      stub_files(files: bad_files, path: 'test_readings_path/*.yml')

      expect(Booklog::ParseReadings).to receive(:puts) do |arg|
        expect(arg).to start_with('YAML Exception reading reading1.yml:')
      end

      Booklog::ParseReadings.call(readings_path: 'test_readings_path', books: books)
    end
  end

  context 'when error reading file' do
    let(:bad_file) do
      {
        'reading1.yml' => <<-EOF,
---
:bad_file: true
---
      EOF

        'reading2.yml' => <<-EOF
---
:sequence: 2
:book_id: book-3-id
:isbn: '9780451150707'
:pages_total: '326'
:pages_read: '326'
:date_started: 2012-05-13
:date_finished: 2012-05-14
      EOF
      }
    end
    it 'writes an error message' do
      stub_files(files: bad_file, path: 'test_readings_path/*.yml')

      original_load = YAML.method(:load)
      expect(YAML).to receive(:load).with("---\n:bad_file: true\n---\n").and_raise(RuntimeError)
      expect(YAML).to receive(:load) do |args|
        original_load.call(args)
      end

      expect(Booklog::ParseReadings).to receive(:puts)
        .with('Error reading reading1.yml: RuntimeError')

      Booklog::ParseReadings.call(readings_path: 'test_readings_path', books: books)
    end
  end
end
