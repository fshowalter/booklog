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
          books.select do |book|
            book.title.match(/.*#{query}.*/i)
          end
        end

        def format_title_results(results:)
          results.map do |book|
            [
              Bold.call(text: book.title),
              format_authors(authors: book.authors),
              "\n"
            ].join
          end
        end

        def format_authors(authors:)
          return unless authors.any?
          "\n   by " + authors.to_sentence
        end
      end
    end
  end
end
