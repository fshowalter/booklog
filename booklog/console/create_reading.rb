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
        def call
          book = ask_for_book
          reading = Booklog::CreateReading.call(**build_reading_data(book: book))

          puts "\n Created Reading ##{Bold.call(text: reading.sequence.to_s)}!\n"

          ap(reading.to_h, ruby19_syntax: true)

          reading
        end

        private

        def build_reading_data(book:)
          {
            book: book,
            pages_read: ask_for_pages_read(total_pages: book.page_count),
            date_started: ask_for_date_started,
            date_finished: ask_for_date_finished
          }
        end

        def ask_for_book
          AskForBook.call(books: Booklog.books.values)
        end

        def ask_for_pages_read(total_pages:)
          pages_read = nil

          while pages_read.nil?
            entered_pages_read = Ask.input 'Pages Read', default: total_pages
            pages_read = entered_pages_read if Ask.confirm entered_pages_read
          end

          pages_read
        end

        def ask_for_page_count
          page_count = nil

          while page_count.nil?
            entered_page_count = Ask.input 'Page Count'
            page_count = entered_page_count if Ask.confirm entered_page_count
          end

          page_count
        end

        def ask_for_date_started
          date = nil
          last_date = Booklog.reviews[Booklog.reviews.length]
          default = last_date.try(:[], :date_finished).to_s

          while date.nil?
            entered_date = Ask.input 'Date Started', default: default
            next unless (entered_date = Date.parse(entered_date))

            date = entered_date if Ask.confirm entered_date.strftime('%A, %B %d, %Y?  ')
          end

          date
        end

        def ask_for_isbn
          isbn = nil

          while isbn.nil?
            entered_isbn = Ask.input 'ISBN'
            isbn = entered_isbn if Ask.confirm entered_isbn
          end

          isbn
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
