# frozen_string_literal: true
module Booklog
  module Console
    #
    # Responsible for providing a console interface for searching and selecting authors.
    #
    class AskForAuthor
      class << self
        def call(authors:)
          result = nil

          while result.nil?
            query = Ask.input 'Author'
            results = search_authors(authors: authors, query: query)
            choices = format_results(results: results) + ['Search Again']
            idx = Ask.list(' Author', choices)

            next if idx == results.length

            result = results[idx]
          end

          result
        end

        private

        def search_authors(authors:, query:)
          authors.sort_by(&:sortable_name).select do |author|
            author.name.match(/.*#{query}.*/i)
          end
        end

        def format_results(results:)
          results.map(&:name_with_annotation)
        end
      end
    end
  end
end
