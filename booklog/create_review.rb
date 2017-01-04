# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new viewing instances.
  #
  class CreateReview
    class << self
      def call(reviews_path:, date:, sequence:, book_id:)
        file_name = File.join(reviews_path, format('%04d', sequence) + '-' + book_id + '.md')

        review = {
          sequence: sequence,
          book_id: book_id,
          date: date,
          grade: ''
        }

        content = "#{review.to_yaml}---\n"
        File.open(file_name, 'w') { |file| file.write(content) }

        OpenStruct.new(review)
      end
    end
  end
end
