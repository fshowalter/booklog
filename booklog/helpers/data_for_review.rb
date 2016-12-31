# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_review(review:)
      {
        data: {
          title: review.title,
          sort_title: review.sortable_title,
          release_date: review.release_date.iso8601,
          release_date_year: review.release_date.year,
          review_date: review.date,
          grade: Booklog::ConvertGradeToNumber.call(grade: review.grade).to_s.rjust(2, '0')
        }
      }
    end
  end
end
