# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreatePlaceholder do
  let(:books) do
    {
      'the-shining-by-stephen-king' => OpenStruct.new(cover: 'cover', cover_placeholder: 'placeholder'),
      'night-shift-by-stephen-king ' => OpenStruct.new(cover: 'cover-url')
    }
  end

  let(:pages) do
    {}
  end

  before(:each) do
    IOHelper.clear
    allow(Booklog).to receive(:books).and_return(books)
    allow(Booklog).to receive(:pages).and_return(pages)
  end

  it 'creates placeholder' do
    IOHelper.type_input("\r")

    expect(Booklog::Console::CreatePlaceholder).to(receive(:puts))
    expect(Booklog::CreatePlaceholder).to(receive(:call).with(image: 'cover-url')) do
      'created placeholder'
    end

    expect(Booklog::Console::CreatePlaceholder.call).to eq 'created placeholder'
  end
end
