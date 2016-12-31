# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Movielog::ParseReviews do
  let(:files) do
    {
      'review1.md' => <<-EOF,
---
:sequence: 5
:title: Black Legion (1937)
:slug: black-legion-1937
:db_title: Black Legion (1937)
:date: 2014-08-22
:grade: C
:imdb_id: tt0027367
---
Review 1 content.
      EOF

      'review2.md' => <<-EOF
---
:sequence: 4
:db_title: Circus of Fear (1966)
:slug: psycho-circus-1967
:title: Psycho-Circus (1967)
:date: 2014-08-11
:imdb_id: tt0060865
:grade: C
---
Review 2 content.
      EOF
    }
  end

  it 'reads reviews from the given directory' do
    stub_files(files: files, path: 'test_reviews_path/*.md')

    reviews = Movielog::ParseReviews.call(reviews_path: 'test_reviews_path')

    expect(reviews.length).to eq 2

    expect(reviews['Black Legion (1937)'].title).to eq 'Black Legion (1937)'
    expect(reviews['Black Legion (1937)'].sequence).to eq 5
    expect(reviews['Black Legion (1937)'].content).to eq "Review 1 content.\n"

    expect(reviews['Circus of Fear (1966)'].db_title).to eq 'Circus of Fear (1966)'
    expect(reviews['Circus of Fear (1966)'].sequence).to eq 4
    expect(reviews['Circus of Fear (1966)'].content).to eq "Review 2 content.\n"
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

      expect(Movielog::ParseReviews).to receive(:puts) do |arg|
        expect(arg).to start_with('YAML Exception reading review1.md:')
      end

      Movielog::ParseReviews.call(reviews_path: 'test_reviews_path')
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
:sequence: 4
:title: Circus of Fear (1966)
:slug: psycho-circus-1967
:display_title: Psycho-Circus (1967)
:date: 2014-08-11
:imdb_id: tt0060865
:grade: C
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

      expect(Movielog::ParseReviews).to receive(:puts)
        .with('Error reading file review1.md: RuntimeError')

      Movielog::ParseReviews.call(reviews_path: 'test_reviews_path')
    end
  end
end
