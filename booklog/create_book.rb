# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new book instances.
  #
  class CreateBook
    class << self
      def call(books_path: Booklog.books_path, title:, sortable_title:, aka_titles:, authors:, isbn:, year_published:)
        id = build_id(title: title, authors: authors)
        file_name = File.join(books_path, id + '.yml')

        front_matter = {
          id: id,
          title: title,
          sortable_title: sortable_title,
          aka_titles: aka_titles,
          author_ids: authors.map(&:id),
          isbn: isbn,
          year_published: year_published
        }

        content = "#{front_matter.to_yaml}\n"

        File.open(file_name, 'w') { |file| file.write(content) }

        OpenStruct.new(front_matter)
      end

      private

      def build_id(title:, authors:)
        author_names = authors.map(&:name).to_sentence

        Booklog::Slugize.call(text: "#{title} by #{author_names}")
      end
    end
  end
end
