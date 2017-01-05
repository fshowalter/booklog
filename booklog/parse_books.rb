# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing reading data.
  #
  class ParseBooks
    class << self
      def call(books_path:)
        Dir["#{books_path}/*.yml"].map do |file|
          book = read_book(file)
          next unless book.is_a?(Hash)
          [book[:isbn], Book.new(book)]
        end.compact.to_h
      end

      private

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
