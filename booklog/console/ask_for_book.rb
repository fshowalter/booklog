# frozen_string_literal: true
module Booklog
  module Console
    #
    # Responsible for providing a console interface for searching and selecting books.
    #
    class AskForBook
      class << self
        def call(books:)
          result = nil

          while result.nil?
            query = Ask.input 'Title'
            results = search_books(books: books, query: query)
            choices = format_title_results(results: results) + ['Search Again']
            idx = Ask.list(' Title', choices)

            next if idx == results.length

            result = results[idx]
          end

          result
        end

        private

        def search_books(books:, query:)
          books.sort_by(&:sortable_title).select do |book|
            book.title.match(/.*#{query}.*/i)
          end
        end

        def format_title_results(results:)
          results.map(&:title_with_author)
        end
      end
    end
  end
end
