module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def grade_to_svg_stars(grade:)
      ConvertGradeToSvgStars.call(grade: grade)
    end

    #
    # Responsible for converting a letter grade into an SVG star graphic.
    #
    class ConvertGradeToSvgStars
      class << self
        def call(grade:)
          return '' if grade.blank?

          '<svg class="rating" xmlns="http://www.w3.org/2000/svg" ' \
          'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 2560 512">' +
          SVG_STARS_FOR_LETTER_GRADE[grade] || '' \
          '</svg>'
        end

        private

        def star(index = 0)
          "<polygon transform=\"translate(#{512 * index})\" class=\"star\" " \
          "points=\"256,389.375 97.781,499.477 153.601,314.977 0,198.523 192.71,194.59 " \
          "256,12.523 319.297,194.59 512,198.523 358.399,314.977 414.226,499.477 \"/>"
        end

        def empty_star(index = 0)
          "<path transform=\"translate(#{512 * index})\" class=\"empty-star\" " \
          "d=\"M 512, 198.52 l -192.709-3.924 L 255.995,12.524 l -63.288,182.071 " \
          'L 0,198.52 l 153.599,116.463 L 97.781,499.476 l 158.214-110.103 ' \
          'l 158.229,110.103 l -55.831-184.493 L 512,198.52 z M 359.202,423.764 ' \
          'L 255.994,351.94 l -103.207,71.823 l 36.414-120.35 L 89.003,227.448 ' \
          'l 125.708-2.566 l 41.292-118.773 l 41.283,118.773 l 125.699,2.566 ' \
          "l -100.2,75.967 L 359.202,423.764 z\"/>"
        end
      end

      SVG_STARS_FOR_LETTER_GRADE = {
        'A' => [star, star(1), star(2), star(3), star(4)].join,
        'B' => [star, star(1), star(2), star(3), empty_star(4)].join,
        'C' => [star, star(1), star(2), empty_star(3), empty_star(4)].join,
        'D' => [star, star(1), empty_star(2), empty_star(3), empty_star(4)].join,
        'F' => [star, empty_star(1), empty_star(2), empty_star(3), empty_star(4)].join
      }
    end
  end
end
