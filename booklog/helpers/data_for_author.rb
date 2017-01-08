# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_author(author:, reviews:)
      {
        data: {
          sort_name: author.sortable_name,
          name: author.name,
          review_count: reviews.length.to_s.rjust(3, '0'),
        },
      }
    end
  end
end
