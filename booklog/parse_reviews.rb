# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing review data.
  #
  class ParseReviews
    class << self
      def call(reviews_path:, books:)
        Dir["#{reviews_path}/*.md"].map do |file|
          review_data = read_file(file: file)
          next unless review_data.is_a?(Hash)

          review = build_review(review_data: review_data, books: books)

          [review.id, review]
        end.compact.to_h
      end

      private

      def build_review(review_data:, books:)
        book_id = review_data.delete(:book_id)
        review_data[:book] = books[book_id]

        Review.new(review_data)
      end

      def read_file(file:)
        content = IO.read(file)
        return unless content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m
        data = YAML.load(Regexp.last_match[1])
        data[:content] = $POSTMATCH
        data

      rescue YAML::SyntaxError => e
        puts "YAML Exception reading #{file}: #{e.message}"
      rescue => e
        puts "Error reading #{file}: #{e.message}"
      end
    end
  end
end
