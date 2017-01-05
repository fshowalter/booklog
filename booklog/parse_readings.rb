# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing reading data.
  #
  class ParseReadings
    class << self
      def call(readings_path:)
        readings = Dir["#{readings_path}/*.yml"].map do |file|
          reading_data = read_reading(file)
          next unless reading_data.is_a?(Hash)
          Reading.new(reading_data)
        end.compact.sort_by(&:sequence)
      end

      private

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
