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

        def create_placeholder(image)
          Booklog::CreatePlaceholder.call(image: image)
        end

        def ask_for_book
          options = build_options
          keys = options.keys

          idx = Ask.list(' Title', keys)

          options[keys[idx]]
        end

        def build_options
          options = {}

          Booklog.books.values.reject(&:cover_placeholder).each do |book|
            options[book.title_with_author] = book.cover
          end

          Booklog.pages.values.reject(&:backdrop_placeholder).each do |page|
            options[page.title] = page.backdrop
          end

          options
        end
      end
    end
  end
end
