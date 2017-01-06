# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreateAuthor do
  before(:each) do
    IOHelper.clear
  end

  it 'calls Booklog::CreateAuthor with correct data' do
    IOHelper.type_input('Joe Author')
    IOHelper.confirm
    IOHelper.select
    IOHelper.confirm
    IOHelper.type_input('https://some.url')
    IOHelper.confirm

    expect(Booklog::Console::CreateAuthor).to receive(:puts).twice

    expect(Booklog::CreateAuthor).to receive(:call).with(
      name: 'Joe Author',
      sortable_name: 'Author, Joe',
      url: 'https://some.url'
    ).and_return(OpenStruct.new(id: 'joe-author'))

    Booklog::Console::CreateAuthor.call
  end
end
