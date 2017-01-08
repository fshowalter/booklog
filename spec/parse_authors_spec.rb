# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Booklog::ParseAuthors do
  let(:files) do
    {
      'author1.yml' => <<-EOF,
---
:id: stephen-king
:name: Stephen King
:name_with_annotation: Stephen King
:sortable_name: King, Stephen
:url: https://en.wikipedia.org/wiki/Stephen_King
      EOF

      'author2.yml' => <<-EOF
---
:id: graham-masterton
:name: Graham Masterton
:name_with_annotation: Graham Masterton
:sortable_name: Masterton, Graham
:url: https://en.wikipedia.org/wiki/Graham_Masterton
      EOF
    }
  end

  it 'reads authors from the given directory' do
    stub_files(files: files, path: 'test_authors_path/*.yml')

    authors = Booklog::ParseAuthors.call(authors_path: 'test_authors_path')

    expect(authors.keys).to eq([
                                 'stephen-king',
                                 'graham-masterton',
                               ])
  end

  context 'when error parsing yaml' do
    let(:bad_files) do
      {
        'author1.yml' => <<-EOF,
---
:id: 1
1:bad
---
        EOF
      }
    end

    it 'writes an error message' do
      stub_files(files: bad_files, path: 'test_authors_path/*.yml')

      expect(Booklog::ParseAuthors).to receive(:puts) do |arg|
        expect(arg).to start_with('YAML Exception reading author1.yml:')
      end

      Booklog::ParseAuthors.call(authors_path: 'test_authors_path')
    end
  end

  context 'when error author file' do
    let(:bad_file) do
      {
        'author1.yml' => <<-EOF,
---
:bad_file: true
---
      EOF

        'author2.yml' => <<-EOF
---
:id: graham-masterton
:name: Graham Masterton
:name_with_annotation: Graham Masterton
:sortable_name: Masterton, Graham
:url: https://en.wikipedia.org/wiki/Graham_Masterton
      EOF
      }
    end
    it 'writes an error message' do
      stub_files(files: bad_file, path: 'test_authors_path/*.yml')

      original_load = YAML.method(:load)
      expect(YAML).to receive(:load).with("---\n:bad_file: true\n---\n").and_raise(RuntimeError)
      expect(YAML).to receive(:load) do |args|
        original_load.call(args)
      end

      expect(Booklog::ParseAuthors).to receive(:puts)
        .with('Error reading author1.yml: RuntimeError')

      Booklog::ParseAuthors.call(authors_path: 'test_authors_path')
    end
  end
end
