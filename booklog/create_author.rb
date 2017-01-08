# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new author instances.
  #
  class CreateAuthor
    class << self
      def call(authors_path: Booklog.authors_path, authors: Booklog.authors, name:, sortable_name:, url:)
        front_matter = build_front_matter(
          authors: authors,
          name: name,
          sortable_name: sortable_name,
          url: url,
        )

        write_file(authors_path: authors_path, front_matter: front_matter)

        OpenStruct.new(front_matter)
      end

      private

      def build_front_matter(authors:, name:, sortable_name:, url:)
        id, name_with_annotation = build_id(name: name, authors: authors)

        {
          id: id,
          name: name.strip,
          name_with_annotation: name_with_annotation,
          sortable_name: sortable_name.strip,
          url: url.strip,
        }
      end

      def write_file(authors_path:, front_matter:)
        file_name = File.join(authors_path, front_matter[:id] + '.yml')

        content = "#{front_matter.to_yaml}\n"

        File.open(file_name, 'w') { |file| file.write(content) }
      end

      def build_id(name:, authors:)
        name_with_annotation = name.strip
        existing_authors = authors.values.select { |a| a.name == name_with_annotation }

        if existing_authors.any?
          name_with_annotation =
            "#{name_with_annotation} (#{Booklog::ConvertIntToRoman.call(existing_authors.length + 1)})"
        end

        Booklog::Slugize.call(text: name_with_annotation)

        [id, name_with_annotation]
      end
    end
  end
end
