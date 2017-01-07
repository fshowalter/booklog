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
        def call(books: Booklog.books, pages: Booklog.pages)
          image = ask_for_image(books: books, pages: pages)
          placeholder = Booklog::CreatePlaceholder.call(image: image)

          puts "\n #{placeholder} \n" \

          placeholder
        end

        private

        def ask_for_image(books:, pages:)
          options = build_options(books: books, pages: pages)
          keys = options.keys.sort

          idx = Ask.list(' Post', keys)

          options[keys[idx]]
        end

        def build_options(books:, pages:)
          options = {}

          books.values.reject(&:cover_placeholder).each do |book|
            options[book.title_with_author] = book.cover
          end

          pages.values.reject(&:backdrop_placeholder).each do |page|
            options[page.title] = page.backdrop
          end

          options
        end
      end
    end
  end
end
