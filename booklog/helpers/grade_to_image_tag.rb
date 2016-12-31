# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def grade_to_image_tag(grade:, options: {})
      return '' if grade.blank?

      file, alt = ImageInfoForGrade.call(grade: grade)

      unless development?
        file = 'https://www.franksmovielog.com/' + image_path(file)
      end

      options[:alt] = alt

      image_tag(file, options)
    end

    #
    # Responsible for providing image tag info for a given grade.
    #
    class ImageInfoForGrade
      INFO_FOR_GRADE = {
        'A' => ['5-stars.svg', '5 Stars (out of 5)'],
        'B' => ['4-stars.svg', '4 Stars (out of 5)'],
        'C' => ['3-stars.svg', '3 Stars (out of 5)'],
        'D' => ['2-stars.svg', '2 Stars (out of 5)'],
        'F' => ['1-star.svg', '1 Star (out of 5)']
      }.freeze

      class << self
        def call(grade:)
          INFO_FOR_GRADE[grade[0]]
        end
      end
    end
  end
end
