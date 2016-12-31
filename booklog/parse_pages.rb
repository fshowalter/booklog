# frozen_string_literal: true
require 'yaml'

module Booklog
  #
  # Responsible for parsing page data.
  #
  class ParsePages
    class << self
      def call(pages_path:)
        Dir["#{pages_path}/*.md"].each_with_object({}) do |file, pages|
          begin
            read_file(file: file, pages: pages)
          rescue YAML::SyntaxError => e
            puts "YAML Exception reading #{file}: #{e.message}"
          rescue => e
            puts "Error reading file #{file}: #{e.message}"
          end
        end
      end

      private

      def read_file(file:, pages:)
        content = IO.read(file)
        return unless content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m
        data = YAML.load(Regexp.last_match[1])
        data[:content] = $POSTMATCH
        pages[data[:slug]] = Page.new(data)
      end
    end
  end
end
