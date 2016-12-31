# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def grade_to_unicode_stars(grade:)
      Movielog::ConvertGradeToUnicodeStars.call(grade: grade)
    end
  end
end
