# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing author data.
  #
  class ParseAuthors
    class << self
      def call(authors_path:)
        Dir["#{authors_path}/*.yml"].map do |file|
          author_data = read_author(file)
          next unless author_data.is_a?(Hash)
          author = Author.new(author_data)
          [author.id, author]
        end.compact.to_h
      end

      private

      def read_author(file)
        YAML.load(IO.read(file))
      rescue YAML::SyntaxError => e
        puts "YAML Exception reading #{file}: #{e.message}"
      rescue => e
        puts "Error reading #{file}: #{e.message}"
      end
    end
  end
end
