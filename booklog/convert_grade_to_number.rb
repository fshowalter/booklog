# frozen_string_literal: true
module Booklog
  #
  # Responsible for converting a letter grade into a number.
  #
  class ConvertGradeToNumber
    NUMBER_FOR_LETTER_GRADE = {
      'A' => 5,
      'B' => 4,
      'C' => 3,
      'D' => 2,
      'F' => 1
    }.freeze
    class << self
      def call(grade:)
        NUMBER_FOR_LETTER_GRADE[grade]
      end
    end
  end
end
