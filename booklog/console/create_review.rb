# frozen_string_literal: true
require 'awesome_print'

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
        # @return [OpenStruct] The new review data.
        def call(books: Booklog.books)
          book = AskForBook.call(books: books.values)
          review = Booklog::CreateReview.call(book: book)

          puts "\n Created Review ##{Bold.call(text: review.sequence.to_s)}!\n"
          ap(review.to_h, ruby19_syntax: true)

          review
        end
      end
    end
  end
end
