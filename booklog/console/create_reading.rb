# frozen_string_literal: true
require 'inquirer'

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

          puts "\n Created Reading ##{Bold.call(text: reading.sequence.to_s)}!\n" \
            " #{Bold.call(text: '         Title:')} #{book.title}\n" \
            " #{Bold.call(text: '        Author:')} #{book.authors.to_sentence}\n" \
            " #{Bold.call(text: '    Pages Read:')} #{reading.pages_read}/#{book.page_count}\n" \
            " #{Bold.call(text: '  Date Started:')} #{reading.date_started}\n" \
            " #{Bold.call(text: ' Date Finished:')} #{reading.date_finished}\n" \

          reading
        end

        private

        def build_reading_data(book:)
          {
            readings_path: Booklog.readings_path,
            sequence: Booklog.next_reading_number,
            book_id: book.id,
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
