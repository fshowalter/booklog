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
          book = AskForBook.call(books: Booklog.books.values)
          review = Booklog::CreateReview.call(book: book)

          puts "\n Created Review ##{Bold.call(text: review.sequence.to_s)}:" \
          "#{book.title_with_author}\n" \

          review
        end
      end
    end
  end
end
