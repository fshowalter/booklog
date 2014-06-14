require 'yaml'

module Booklog
  #
  # Responsible for parsing review data.
  #
  class ParseReviews
    class << self
      def call(reviews_path)
        Dir["#{reviews_path}/*.md"].reduce({}) do |memo, file|
          begin
            read_file(memo, file)
          rescue SyntaxError => e
            puts "YAML Exception reading #{file}: #{e.message}"
          rescue => e
            puts "Error reading file #{file}: #{e.message}"
          end
        end
      end

      private

      def read_file(hash, file)
        content = IO.read(file)
        return unless content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m

        data = YAML.load(Regexp.last_match[1])
        data[:content] = $POSTMATCH
        hash[data[:sequence]] = Review.new(data)
        hash
      end
    end
  end
end
