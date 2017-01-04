# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreatePage do
  before(:each) do
    IOHelper.clear
    allow(File).to receive(:open).and_call_original
    allow(File).to receive(:open).with(Booklog.pages_path + '/test-page.md', 'w')
  end

  it 'creates pages with titles and date' do
    IOHelper.type_input('test page')
    IOHelper.confirm

    expect(Booklog::Console::CreatePage).to(receive(:puts))

    page = Booklog::Console::CreatePage.call

    expect(page.title).to eq 'test page'
    expect(page.date).to eq Date.today
    expect(page.slug).to eq 'test-page'
  end
end
