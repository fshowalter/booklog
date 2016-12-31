# frozen_string_literal: true
module Booklog
  #
  # Responsible for converting a letter grade into a unicode star sequence.
  #
  class ConvertGradeToUnicodeStars
    UNICODE_STAR_FOR_LETTER_GRADE = {
      'A' => '★★★★★',
      'B' => '★★★★☆',
      'C' => '★★★☆☆',
      'D' => '★★☆☆☆',
      'F' => '★☆☆☆☆'
    }.freeze
    class << self
      def call(grade:)
        UNICODE_STAR_FOR_LETTER_GRADE[grade]
      end
    end
  end
end
