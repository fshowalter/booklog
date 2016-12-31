# frozen_string_literal: true
module Booklog
  #
  # Responsible for converting text to a format suitable for use in a url.
  #
  class Slugize
    class << self
      def call(text:, replacement: '-')
        slugged = text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '?')
        slugged.gsub!('&', 'and')
        slugged.delete!(':')
        slugged.gsub!(/[^\w_\-#{Regexp.escape(replacement)}]+/i, replacement)
        slugged.gsub!(/#{replacement}{2,}/i, replacement)
        slugged.gsub!(/^#{replacement}|#{replacement}$/i, '')
        url_encode(text: slugged.downcase)
      end

      private

      def url_encode(text:)
        URI.escape(text, /[^\w+-]/i)
      end
    end
  end
end
