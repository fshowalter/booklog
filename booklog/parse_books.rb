# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing reading data.
  #
  class ParseBooks
    class << self
      def call(books_path:)
        Dir["#{books_path}/*.yml"].each_with_object({}) do |file, books|
          book = read_book(file)
          next unless book.is_a?(Hash)
          books[book[:id]] = Book.new(book)
        end
      end

      private

      def read_book(file)
        YAML.load(IO.read(file))
      rescue YAML::SyntaxError => e
        puts "YAML Exception reading #{file}: #{e.message}"
      rescue => e
        puts "Error reading file #{file}: #{e.message}"
      end
    end
  end
end
