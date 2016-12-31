# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_reading(reading:)
      {
        data: {
          title: reading.title,
          sort_title: reading.sortable_title,
          date_published: reading.date_published.iso8601,
          date_published_year: reading.date_published.year,
          date_started: reading.date_started,
          date_finished: reading.date_finished
        }
      }
    end
  end
end
