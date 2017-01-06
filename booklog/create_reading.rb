# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new reading instances.
  #
  class CreateReading
    class << self
      #
      # Responsible for creating a new reading instance.
      #
      def call(
        readings_path: Booklog.readings_path,
        sequence: Booklog.next_reading_number,
        book:,
        pages_read:,
        date_started:,
        date_finished:
      )

        file_name = File.join(readings_path, format('%04d', sequence) + '-' + book.slug + '.yml')

        reading = {
          sequence: sequence,
          isbn: book.isbn,
          pages_read: pages_read,
          date_started: date_started,
          date_finished: date_finished
        }

        File.open(file_name, 'w') { |file| file.write(reading.to_yaml) }

        OpenStruct.new(reading)
      end
    end
  end
end
