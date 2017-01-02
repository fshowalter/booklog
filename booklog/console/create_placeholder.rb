# frozen_string_literal: true
module Booklog
  module Console
    #
    # Responsible for providing a console interface to create new placeholder images.
    #
    class CreatePlaceholder
      class << self
        #
        # Responsible for providing a console interface to create a new placeholder image.
        #
        # @return the base64 encoded placeholder
        def call
          book = ask_for_book
          placeholder = create_placeholder(book)

          puts "\n #{placeholder} \n" \

          placeholder
        end

        private

        def create_placeholder(book)
          Booklog::CreatePlaceholder.call(image: book.cover)
        end

        def ask_for_book
          books_without_placeholder = Booklog.books.values.reject(&:cover_placeholder)

          options = books_without_placeholder.map { |b| "#{b.title} by #{b.authors.to_sentence}"}

          idx = Ask.list(' Title', options)

          books_without_placeholder[idx]
        end
      end
    end
  end
end
