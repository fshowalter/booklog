# frozen_string_literal: true
require 'active_support/core_ext/object/try'
require 'active_support/core_ext/array/conversions'

module Booklog
  #
  # Namespace for booklog console use-cases.
  #
  module Console
    #
    # Responsible for providing a command-line interface to create new reviews.
    #
    class CreateReview
      class << self
        #
        # Responsible for processing a new review command.
        #
        # @return [String] The full path to the new entry.
        def call
          book = ask_for_book
          review = Booklog::CreateReview.call(**build_review_data(book: book))

          puts "\n Created Review ##{Bold.call(text: review.sequence.to_s)}!\n" \
          " #{Bold.call(text: ' Title:')} #{book.title}\n" \
          " #{Bold.call(text: ' Author:')} #{book.authors.to_sentence}\n" \

          review
        end

        private

        def build_review_data(book:)
          {
            reviews_path: Booklog.reviews_path,
            date: Date.today,
            sequence: Booklog.next_review_number,
            book_id: book.id
          }
        end

        def ask_for_book
          AskForBook.call(books: Booklog.books.values)
        end
      end
    end
  end
end
