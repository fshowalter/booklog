# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing reading data.
  #
  class ParseBooks
    class << self
      def call(books_path:, authors:)
        Dir["#{books_path}/*.yml"].map do |file|
          book_data = read_book(file)
          next unless book_data.is_a?(Hash)
          book = build_book(book_data: book_data, authors: authors)
          [book.id, book]
        end.compact.to_h
      end

      private

      def build_book(book_data:, authors:)
        author_ids = book_data.delete(:author_ids)
        book_data[:authors] = author_ids.map { |id| authors[id] }

        Book.new(book_data)
      end

      def read_book(file)
        YAML.load(IO.read(file))
      rescue YAML::SyntaxError => e
        puts "YAML Exception reading #{file}: #{e.message}"
      rescue => e
        puts "Error reading #{file}: #{e.message}"
      end
    end
  end
end
