# frozen_string_literal: true
require 'spec_helper'

describe Booklog::CreateAuthor do
  let(:authors) do
    {
      'test-author' => OpenStruct.new(name: 'Test Author'),
      'test-author-ii' => OpenStruct.new(name: 'Test Author'),
    }
  end

  it('creates author') do
    allow(File).to receive(:open).with('test-authors-path' + '/test-author-iii.yml', 'w')

    expect(Booklog::CreateAuthor.call(
      authors_path: 'test-authors-path',
      authors: authors,
      name: 'Test Author',
      sortable_name: 'Author, Test',
      url: 'https://author.url',
    ).to_h).to eq(
      id: 'test-author-iii',
      name: 'Test Author',
      name_with_annotation: 'Test Author (III)',
      sortable_name: 'Author, Test',
      url: 'https://author.url',
    )
  end
end
