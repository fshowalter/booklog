# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def oldest_year(collection:, date_method:)
      return unless collection&.any?

      collection.map(&date_method).sort.first.year
    end
  end
end
