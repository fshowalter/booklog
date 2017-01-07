# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreatePage do
  before(:each) do
    IOHelper.clear
  end

  it 'calls Booklog::CreatePage with correct data' do
    IOHelper.type_input('Test Page')
    IOHelper.confirm

    expect(Booklog::Console::CreatePage).to(receive(:puts)).twice

    expect(Booklog::CreatePage).to receive(:call).with(
      title: 'Test Page',
    ).and_return(OpenStruct.new(title: 'New Page Title'))

    Booklog::Console::CreatePage.call
  end
end
