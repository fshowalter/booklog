# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing reading data.
  #
  class ParseReadings
    class << self
      def call(readings_path:)
        Dir["#{readings_path}/*.yml"].each_with_object({}) do |file, readings|
          reading = read_reading(file)
          next unless reading.is_a?(Hash)
          readings[reading[:number]] = OpenStruct.new(reading)
        end
      end

      private

      def read_reading(file)
        YAML.load(IO.read(file))
      rescue YAML::SyntaxError => e
        puts "YAML Exception reading #{file}: #{e.message}"
      rescue => e
        puts "Error reading file #{file}: #{e.message}"
      end
    end
  end
end
