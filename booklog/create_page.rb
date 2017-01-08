# frozen_string_literal: true
require 'active_support/core_ext/hash/slice'

module Booklog
  #
  # Responsible for creating new pages.
  #
  class CreatePage
    class << self
      def call(pages_path: Booklog.pages_path, title:)
        front_matter = build_front_matter(title: title)

        write_file(pages_path: pages_path, front_matter: front_matter)

        OpenStruct.new(front_matter)
      end

      private

      def build_front_matter(title:)
        id = Booklog::Slugize.call(text: title)

        {
          id: id,
          title: title,
          date: Date.today,
        }
      end

      def write_file(pages_path:, front_matter:)
        file_name = File.join(pages_path, front_matter[:id] + '.md')

        content = "#{front_matter.to_yaml}---\n"

        File.open(file_name, 'w') { |file| file.write(content) }
      end
    end
  end
end
