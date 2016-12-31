# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Movielog::Console::CreatePage do
  before(:each) do
    IOHelper.clear
    allow(File).to receive(:open).with(Movielog.pages_path + '/test-page.md', 'w')
  end

  it 'creates pages with titles and date' do
    IOHelper.type_input('test page')
    IOHelper.confirm

    expect(Movielog::Console::CreatePage).to(receive(:puts))
    expect(Movielog).to receive(:next_post_number).and_return(2)

    page = Movielog::Console::CreatePage.call

    expect(page.title).to eq 'test page'
    expect(page.sequence).to eq 2
    expect(page.slug).to eq 'test-page'
  end
end
