# frozen_string_literal: true
require 'active_support/core_ext/hash/slice'

module Booklog
  #
  # Responsible for creating new pages.
  #
  class CreatePage
    class << self
      def call(pages_path:, title:, sequence:, slug:)
        file_name = new_page_file_name(pages_path, slug)

        front_matter = {
          title: title,
          sequence: sequence,
          slug: slug,
          date: Date.today
        }

        content = "#{front_matter.to_yaml}---\n"
        File.open(file_name, 'w') { |file| file.write(content) }

        Page.new(front_matter)
      end

      private

      def new_page_file_name(pages_path, slug)
        File.join(pages_path, slug + '.md')
      end
    end
  end
end
