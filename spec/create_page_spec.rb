# frozen_string_literal: true
require 'spec_helper'

describe Booklog::CreatePage do
  it('creates page') do
    allow(File).to receive(:open).with('test-pages-path' + '/test-page.md', 'w')

    expect(Booklog::CreatePage.call(
      pages_path: 'test-pages-path',
      title: 'Test Page',
    ).to_h).to eq(
      id: 'test-page',
      title: 'Test Page',
      date: Date.today,
      backdrop: '',
      backdrop_placeholder: nil,
    )
  end
end
