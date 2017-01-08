# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new viewing instances.
  #
  class CreateReview
    class << self
      def call(
          reviews_path: Booklog.reviews_path,
          sequence: Booklog.next_review_sequence,
          book:
      )
        front_matter = {
          sequence: sequence,
          book_id: book.id,
          date: Date.today,
          grade: '',
          cover: '',
          cover_placeholder: nil,
        }

        write_file(reviews_path: reviews_path, front_matter: front_matter)

        OpenStruct.new(front_matter)
      end

      private

      def write_file(reviews_path:, front_matter:)
        file_name = File.join(
          reviews_path,
          format('%04d', front_matter[:sequence]) + '-' + front_matter[:book_id] + '.md',
        )

        content = "#{front_matter.to_yaml}---\n"

        File.open(file_name, 'w') { |file| file.write(content) }
      end
    end
  end
end
