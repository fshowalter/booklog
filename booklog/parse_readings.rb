# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing reading data.
  #
  class ParseReadings
    class << self
      def call(readings_path:, books:)
        Dir["#{readings_path}/*.yml"].map do |file|
          reading_data = read_reading(file)
          next unless reading_data.is_a?(Hash)
          build_reading(reading_data: reading_data, books: books)
        end.compact.sort_by(&:sequence)
      end

      private

      def build_reading(reading_data:, books:)
        book_id = reading_data.delete(:book_id)
        reading_data[:book] = books[book_id]

        Reading.new(reading_data)
      end

      def read_reading(file)
        YAML.load(IO.read(file))
      rescue YAML::SyntaxError => e
        puts "YAML Exception reading #{file}: #{e.message}"
      rescue => e
        puts "Error reading #{file}: #{e.message}"
      end
    end
  end
end
