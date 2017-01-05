# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new book instances.
  #
  class CreateBook
    class << self
      def call(books_path: Booklog.books_path, title:, aka_titles:, authors:, page_count:, year_published:, isbn:)
        id = build_id(title: title, authors: authors)
        file_name = File.join(books_path, id + '.yml')

        front_matter = {
          id: id,
          title: title,
          aka_titles: aka_titles,
          authors: authors,
          page_count: page_count,
          year_published: year_published,
          isbn: isbn,
          cover: '',
          cover_placeholder: nil
        }

        content = "#{front_matter.to_yaml}\n"

        File.open(file_name, 'w') { |file| file.write(content) }

        OpenStruct.new(front_matter)
      end

      private

      def build_id(title:, authors:)
        author_slug = authors.map { |a| Author.new(sortable_name: a).slug }.to_sentence

        Booklog::Slugize.call(text: "#{title} by #{author_slug}")
      end
    end
  end
end
