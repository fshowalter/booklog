# frozen_string_literal: true
require 'spec_helper'
require 'open-uri'
require 'base64'

describe Movielog::CreatePlaceholder do
  it('creates base64 encoded placeholder') do
    expect(Movielog::CreatePlaceholder).to receive(:open).with('test-image-uri') do
      OpenStruct.new(read: 'image data')
    end

    expect(IO).to receive(:popen) do |&block|
      clipboard = []
      block.call(clipboard)
      expect(clipboard[0]).to eq('data:image/jpeg;base64,aW1hZ2UgZGF0YQ==')
    end

    expect(Movielog::CreatePlaceholder.call(image: 'test-image-uri')).to eq(
      'data:image/jpeg;base64,aW1hZ2UgZGF0YQ=='
    )
  end
end
