# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_files_helper'

describe Movielog::ParseViewings do
  let(:files) do
    {
      'viewing1.yml' => <<-EOF,
---
:number: 5
:title: Black Legion (1937)
:display_title: Black Legion (1937)
:date: 2014-08-22
:venue: TCM HD
---
      EOF

      'viewing2.yml' => <<-EOF
---
:number: 4
:title: Circus of Fear (1966)
:display_title: Psycho-Circus (1967)
:date: 2014-08-11
:venue: DVD
---
      EOF
    }
  end

  it 'reads reviews from the given directory' do
    stub_files(files: files, path: 'test_viewings_path/*.yml')

    viewings = Movielog::ParseViewings.call(viewings_path: 'test_viewings_path')

    expect(viewings.length).to eq 2

    expect(viewings[5].title).to eq 'Black Legion (1937)'
    expect(viewings[5].number).to eq 5

    expect(viewings[4].title).to eq 'Circus of Fear (1966)'
    expect(viewings[4].number).to eq 4
  end

  context 'when error parsing yaml' do
    let(:bad_files) do
      {
        'viewing1.yml' => <<-EOF,
---
:sequence: 1
1:bad
---
        EOF
      }
    end

    it 'writes an error message' do
      stub_files(files: bad_files, path: 'test_viewings_path/*.yml')

      expect(Movielog::ParseViewings).to receive(:puts) do |arg|
        expect(arg).to start_with('YAML Exception reading viewing1.yml:')
      end

      Movielog::ParseViewings.call(viewings_path: 'test_viewings_path')
    end
  end

  context 'when error reading file' do
    let(:bad_file) do
      {
        'viewing1.yml' => <<-EOF,
---
:bad_file: true
---
      EOF

        'viewing2.yml' => <<-EOF
---
:number: 4
:title: Circus of Fear (1966)
:display_title: Psycho-Circus (1967)
:date: 2014-08-11
:venue: DVD
---
      EOF
      }
    end
    it 'writes an error message' do
      stub_files(files: bad_file, path: 'test_viewings_path/*.yml')

      original_load = YAML.method(:load)
      expect(YAML).to receive(:load).with("---\n:bad_file: true\n---\n").and_raise(RuntimeError)
      expect(YAML).to receive(:load) do |args|
        original_load.call(args)
      end

      expect(Movielog::ParseViewings).to receive(:puts)
        .with('Error reading file viewing1.yml: RuntimeError')

      Movielog::ParseViewings.call(viewings_path: 'test_viewings_path')
    end
  end
end
