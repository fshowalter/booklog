# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Movielog::Console::CreatePlaceholder do
  let(:reviews) do
    {
      'Rio Bravo' => OpenStruct.new(backdrop: 'backdrop', backdrop_placeholder: 'placeholder'),
      'Fright Night ' => OpenStruct.new(backdrop: 'backdrop-url')
    }
  end

  before(:each) do
    IOHelper.clear
    allow(Movielog).to receive(:reviews).and_return(reviews)
  end

  it 'creates placeholder' do
    IOHelper.type_input("\r")

    expect(Movielog::Console::CreatePlaceholder).to(receive(:puts))
    expect(Movielog::CreatePlaceholder).to(receive(:call).with(image: 'backdrop-url')) do
      'created placeholder'
    end

    expect(Movielog::Console::CreatePlaceholder.call).to eq 'created placeholder'
  end
end
