# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing review data.
  #
  class ParseReviews
    class << self
      def call(reviews_path:)
        Dir["#{reviews_path}/*.md"].map() do |file|
          review = read_file(file: file)
          next unless review.is_a?(Review)

          [review.book_id, review]
        end.compact.to_h
      end

      private

      def read_file(file:)
        content = IO.read(file)
        return unless content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m
        data = YAML.load(Regexp.last_match[1])
        data[:content] = $POSTMATCH
        Review.new(**data)

        rescue YAML::SyntaxError => e
          puts "YAML Exception reading #{file}: #{e.message}"
        rescue => e
          puts "Error reading #{file}: #{e.message}"
      end
    end
  end
end
