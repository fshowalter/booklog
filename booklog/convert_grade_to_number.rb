# frozen_string_literal: true
module Booklog
  #
  # Responsible for converting a letter grade into a number.
  #
  class ConvertGradeToNumber
    NUMBER_FOR_LETTER_GRADE = {
      'A+' => 17,
      'A' => 16,
      'A-' => 15,
      'B+' => 14,
      'B' => 13,
      'B-' => 12,
      'C+' => 11,
      'C' => 10,
      'C-' => 9,
      'D+' => 8,
      'D' => 7,
      'D-' => 6,
      'F' => 5,
    }.freeze
    class << self
      def call(grade:)
        NUMBER_FOR_LETTER_GRADE[grade]
      end
    end
  end
end
