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
    }
    class << self
      def call(grade: grade)
        UNICODE_STAR_FOR_LETTER_GRADE[grade]
      end
    end
  end
end
