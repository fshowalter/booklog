# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_reading(reading:)
      {
        data: {
          title: reading.title_with_author,
          sort_title: reading.sortable_title,
          year_published: reading.year_published,
          date_started: reading.date_started,
          date_finished: reading.date_finished
        }
      }
    end
  end
end
