# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_review(book:, review:)
      {
        data: {
          title: book.title,
          sort_title: book.sortable_title,
          isbn: book.isbn,
          year_published: book.year_published,
          review_date: review.date,
          grade: Booklog::ConvertGradeToNumber.call(grade: review.grade).to_s.rjust(2, '0')
        }
      }
    end
  end
end
