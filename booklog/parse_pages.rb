# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing page data.
  #
  class ParsePages
    class << self
      def call(pages_path:)
        pages = Dir["#{pages_path}/*.md"].map do |file|
          page = read_file(file: file)
          next unless page.is_a?(Page)
          [page.slug, page]
        end.compact.to_h
      end

      private

      def read_file(file:)
        content = IO.read(file)
        return unless content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m

        data = YAML.load(Regexp.last_match[1])
        data[:content] = $POSTMATCH
        Page.new(data)

        rescue YAML::SyntaxError => e
          puts "YAML Exception reading #{file}: #{e.message}"
        rescue => e
          puts "Error reading #{file}: #{e.message}"
      end
    end
  end
end
