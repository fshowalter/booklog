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

        file_name = File.join(reviews_path, format('%04d', sequence) + '-' + book.slug + '.md')

        review = {
          sequence: sequence,
          book_id: book.id,
          date: Date.today,
          grade: '',
          cover: '',
          cover_placeholder: nil
        }

        content = "#{review.to_yaml}---\n"
        File.open(file_name, 'w') { |file| file.write(content) }

        OpenStruct.new(review)
      end
    end
  end
end
