# frozen_string_literal: true
require 'open-uri'
require 'base64'

module Booklog
  #
  # Responsible for creating new placeholder instances.
  #
  class CreatePlaceholder
    class << self
      def call(image:, width: 20, quality: 20)
        small_image = image.gsub(/w\d{3,4}-l\d{2,3}/, "w#{width}-l#{quality}")
        placeholder = "data:image/jpeg;base64,#{Base64.strict_encode64(open(small_image).read)}"

        IO.popen('pbcopy', 'w') { |f| f << placeholder }

        placeholder
      end
    end
  end
end
