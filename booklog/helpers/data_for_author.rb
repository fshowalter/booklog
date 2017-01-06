# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_author(author:)
      {
        data: {
          sort_name: author.sortable_name,
          name: author.name,
          review_count: Booklog.reviews_by_author[author.id].length.to_s.rjust(3, '0')
        }
      }
    end
  end
end
