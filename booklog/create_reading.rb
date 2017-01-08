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
      def call( # rubocop:disable Metrics/MethodLength
        readings_path: Booklog.readings_path,
        sequence: Booklog.next_reading_sequence,
        book:,
        isbn:,
        pages_total:,
        pages_read:,
        date_started:,
        date_finished:
      )
        front_matter = {
          sequence: sequence,
          book_id: book.id,
          isbn: isbn,
          pages_total: pages_total,
          pages_read: pages_read,
          date_started: date_started,
          date_finished: date_finished,
        }

        write_file(readings_path: readings_path, front_matter: front_matter)

        OpenStruct.new(front_matter)
      end

      private

      def write_file(readings_path:, front_matter:)
        file_name = File.join(
          readings_path,
          format('%04d', front_matter[:sequence]) + '-' + front_matter[:book_id] + '.yml',
        )

        content = "#{front_matter.to_yaml}\n"

        File.open(file_name, 'w') { |file| file.write(content) }
      end
    end
  end
end
