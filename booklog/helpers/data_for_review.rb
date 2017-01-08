# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_review(review:)
      {
        data: {
          title: review.title_with_author,
          sort_title: review.sortable_title,
          year_published: review.year_published,
          review_date: review.date,
          grade: Booklog::ConvertGradeToNumber.call(grade: review.grade).to_s.rjust(2, '0'),
        },
      }
    end
  end
end
