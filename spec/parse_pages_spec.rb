# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Movielog::ParsePages do
  let(:files) do
    {
      'page1.md' => <<-EOF,
---
:sequence: 1
:title: Page 1
:slug: page-1
:date: 2014-07-01
---
Page 1 content.
      EOF

      'page2.md' => <<-EOF
---
:sequence: 2
:title: Page 2
:slug: page-2
:date: 2014-07-01
---
Page 2 content.
      EOF
    }
  end

  it 'reads pages from the given directory' do
    stub_files(files: files, path: 'test_pages_path/*.md')

    pages = Movielog::ParsePages.call(pages_path: 'test_pages_path')

    expect(pages.length).to eq 2

    expect(pages['page-1'].title).to eq 'Page 1'
    expect(pages['page-1'].sequence).to eq 1
    expect(pages['page-1'].content).to eq "Page 1 content.\n"

    expect(pages['page-2'].title).to eq 'Page 2'
    expect(pages['page-2'].sequence).to eq 2
    expect(pages['page-2'].content).to eq "Page 2 content.\n"
  end

  context 'when error parsing yaml' do
    let(:bad_files) do
      {
        'page1.md' => <<-EOF,
---
:sequence: 1
1:bad
---
Page 1 content.
        EOF
      }
    end

    it 'writes an error message' do
      stub_files(files: bad_files, path: 'test_pages_path/*.md')

      expect(Movielog::ParsePages).to receive(:puts) do |arg|
        expect(arg).to start_with('YAML Exception reading page1.md:')
      end

      Movielog::ParsePages.call(pages_path: 'test_pages_path')
    end
  end

  context 'when error reading file' do
    let(:bad_file) do
      {
        'page1.md' => <<-EOF,
---
:bad_file: true
---
Page 1 content.
      EOF

        'page2.md' => <<-EOF
---
:sequence: 2
:title: Page 2
:slug: page-2
:date: 2014-07-01
---
Page 2 content.
        EOF
      }
    end
    it 'writes an error message' do
      stub_files(files: bad_file, path: 'test_pages_path/*.md')

      original_load = YAML.method(:load)
      expect(YAML).to receive(:load).with("---\n:bad_file: true\n").and_raise(RuntimeError)
      expect(YAML).to receive(:load) do |args|
        original_load.call(args)
      end

      expect(Movielog::ParsePages).to receive(:puts)
        .with('Error reading file page1.md: RuntimeError')

      Movielog::ParsePages.call(pages_path: 'test_pages_path')
    end
  end
end
