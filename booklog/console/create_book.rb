# frozen_string_literal: true
require 'active_support/core_ext/object/try'
require 'active_support/core_ext/array/conversions'

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

          puts "\n Created Book \"#{Bold.call(text: book.id)}\"!\n" \
          " #{Bold.call(text: '         Title:')} #{book.title}\n" \
          " #{Bold.call(text: '           AKA:')} #{book.aka_titles.to_sentence}\n" \
          " #{Bold.call(text: '       Authors:')} #{book.authors.to_sentence}\n" \
          " #{Bold.call(text: '    Page Count:')} #{book.page_count}\n" \
          " #{Bold.call(text: 'Year Published:')} #{book.year_published}\n" \
          " #{Bold.call(text: '          ISBN:')} #{book.isbn}\n" \

          book
        end

        private

        def build_book_data
          title = ask_for_title

          {
            title: title,
            aka_titles: ask_for_aka_titles,
            authors: ask_for_authors,
            page_count: ask_for_page_count,
            year_published: ask_for_year_published,
            isbn: ask_for_isbn
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

        def ask_for_aka_titles
          aka_titles = []

          while Ask.confirm 'Add AKA Title', default: false
            title = Ask.input 'AKA Titles'
            aka_titles << title if Ask.confirm title
          end

          aka_titles
        end

        def ask_for_authors
          authors = []
          add_authors = true

          while add_authors
            author = Ask.input 'Author [Last Name, First Name (Annotation)]'
            authors << author if Ask.confirm author
            add_authors = Ask.confirm 'Add More Authors', default: false
          end

          authors
        end

        def ask_for_page_count
          page_count = nil

          while page_count.nil?
            entered_page_count = Ask.input 'Page Count'
            page_count = entered_page_count if Ask.confirm entered_page_count
          end

          page_count
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
