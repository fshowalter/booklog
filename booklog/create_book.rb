# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new book instances.
  #
  class CreateBook
    class << self
      def call(books_path:, id:, title:, aka_titles:, authors:, page_count:, year_published:, isbn:)
        file_name = File.join(books_path, id + '.yml')

        front_matter = {
          id: id,
          title: title,
          aka_titles: aka_titles,
          authors: authors,
          page_count: page_count,
          year_published: year_published,
          isbn: isbn
        }

        content = "#{front_matter.to_yaml}\n"

        File.open(file_name, 'w') { |file| file.write(content) }

        OpenStruct.new(front_matter)
      end
    end
  end
end
