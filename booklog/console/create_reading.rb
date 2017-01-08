# frozen_string_literal: true
require 'inquirer'
require 'awesome_print'

module Booklog
  module Console
    #
    # Responsible for providing a console interface to create new readings.
    #
    class CreateReading
      class << self
        #
        # Responsible for processing a new reading command.
        #
        # @return [Hash] The new reading.
        def call(books: Booklog.books)
          book = AskForBook.call(books: books.values)
          reading = Booklog::CreateReading.call(**build_reading_data(book: book))

          puts "\n Created Reading ##{Bold.call(text: reading.sequence.to_s)}!\n"

          ap(reading.to_h, ruby19_syntax: true)

          reading
        end

        private

        def build_reading_data(book:)
          isbn = ask_for_isbn(book: book)
          pages_read, pages_total = ask_for_pages

          {
            book: book,
            isbn: isbn,
            pages_total: pages_total,
            pages_read: pages_read,
            date_started: ask_for_date_started,
            date_finished: ask_for_date_finished,
          }
        end

        def ask_for_isbn(book:)
          isbn = nil

          while isbn.nil?
            entered_isbn = Ask.input 'ISBN', default: book.isbn
            isbn = entered_isbn if Ask.confirm entered_isbn
          end

          isbn
        end

        def ask_for_pages
          page_count = nil
          pages_read, pages_total = nil

          while page_count.nil?
            entered_page_count = Ask.input 'Page Count'

            pages_read, pages_total = entered_page_count.split('/')

            pages_total ||= pages_read

            page_count = entered_page_count if Ask.confirm("Read #{pages_read} of #{pages_total}")
          end

          [pages_read, pages_total]
        end

        def ask_for_date_started
          date = nil

          while date.nil?
            entered_date = Ask.input 'Date Started'
            next unless (entered_date = Date.parse(entered_date))

            date = entered_date if Ask.confirm entered_date.strftime('%A, %B %d, %Y?  ')
          end

          date
        end

        def ask_for_date_finished
          default = Date.today.to_s

          date = nil

          while date.nil?
            entered_date = Ask.input 'Date Finished', default: default
            next unless (entered_date = Date.parse(entered_date))

            date = entered_date if Ask.confirm entered_date.strftime('%A, %B %d, %Y?  ')
          end

          date
        end
      end
    end
  end
end
