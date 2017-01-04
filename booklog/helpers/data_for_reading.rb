# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_reading(book:, reading:)
      {
        data: {
          title: book.title,
          isbn: book.isbn,
          sort_title: book.sortable_title,
          year_published: book.year_published,
          date_started: reading.date_started,
          date_finished: reading.date_finished
        }
      }
    end
  end
end
