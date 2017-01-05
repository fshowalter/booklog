# frozen_string_literal: true
module Booklog
  #
  # Responsible for stubbing review/viewing/feature files.
  #
  module StubFilesHelper
    def stub_files(files:, path:)
      expect(Dir).to receive(:[]).with(path) do
        stub_dir_enumerable(files: files.keys)
      end

      files.each do |key, value|
        expect(IO).to receive(:read).with(key).and_return(value)
      end
    end

    def stub_dir_enumerable(files:)
      enumerable_stub = double('enumerable')
      expect(enumerable_stub).to receive(:map) do |&block|
        files.map { |file| block.call(file) }
      end

      enumerable_stub
    end
  end
end

RSpec.configure do |config|
  config.include(Booklog::StubFilesHelper)
end
