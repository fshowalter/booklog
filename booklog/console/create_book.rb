# frozen_string_literal: true
require 'awesome_print'

module Booklog
  #
  # Namespace for booklog console use-cases.
  #
  module Console
    #
    # Responsible for providing a command-line interface to create new books.
    #
    class CreateBook
      class << self
        #
        # Responsible for processing a new book command.
        #
        # @return [String] The full path to the new entry.
        def call
          book = Booklog::CreateBook.call(**build_book_data)

          puts "\n Created Book ##{Bold.call(text: book.id)}!\n"
          ap(book.to_h, ruby19_syntax: true)

          book
        end

        private

        def build_book_data
          title = ask_for_title

          {
            title: title,
            sortable_title: ask_for_sortable_title(title: title),
            aka_titles: ask_for_aka_titles,
            authors: ask_for_authors,
            isbn: ask_for_isbn,
            year_published: ask_for_year_published
          }
        end

        def ask_for_title
          title = nil

          while title.nil?
            entered_title = Ask.input 'Title'
            title = entered_title if Ask.confirm entered_title
          end

          title
        end

        def ask_for_sortable_title(title:)
          sortable_title = nil

          while sortable_title.nil?
            entered_title = Ask.input 'Sortable Title', default: build_sortable_title(title: title)
            sortable_title = entered_title if Ask.confirm entered_title
          end

          sortable_title
        end

        def build_sortable_title(title:)
          @sortable_title_regex ||= Regexp.new("^('|(?:[Tt]he|[Aa]n?)\\s)")

          if (sortable_match = @sortable_title_regex.match(title))
            sortable_match.post_match + ", #{sortable_match[1].strip}"
          else
            title
          end
        end

        def ask_for_aka_titles
          aka_titles = []

          while Ask.confirm 'Add AKA Title', default: false
            title = Ask.input 'AKA Titles'
            aka_titles << title if Ask.confirm title
          end

          aka_titles
        end

        def ask_for_authors
          authors = [AskForAuthor.call(authors: Booklog.authors.values)]

          while Ask.confirm 'Add Author', default: false
            authors << AskForAuthor.call(authors: Booklog.authors.values)
          end

          authors
        end

        def ask_for_year_published
          year_published = nil

          while year_published.nil?
            entered_year = Ask.input 'Year Published'

            year_published = entered_year if Ask.confirm entered_year
          end

          year_published
        end

        def ask_for_isbn
          isbn = nil

          while isbn.nil?
            entered_isbn = Ask.input 'ISBN'
            isbn = entered_isbn if Ask.confirm entered_isbn
          end

          isbn
        end
      end
    end
  end
end
