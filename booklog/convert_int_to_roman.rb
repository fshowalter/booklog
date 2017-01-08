# frozen_string_literal: true
module Booklog
  #
  # Responsible for converting an int to a roman numeral.
  #
  class ConvertIntToRoman
    DIGITS = {
      'I' => 1,
      'V' => 5,
      'X' => 10,
      'L' => 50,
      'C' => 100,
      'D' => 500,
      'M' => 1000,
    }.freeze

    @digits_lookup = DIGITS.inject(
      4 => 'IV',
      9 => 'IX',
      40 => 'XL',
      90 => 'XC',
      400 => 'CD',
      900 => 'CM',
    ) { |acc, elem| acc.update(elem.last => elem.first) }

    class << self
      def call(int)
        raise if int.negative? || int > 3999
        remainder = int

        @digits_lookup.keys.sort.reverse.each_with_object('') do |digit_value, result|
          while remainder >= digit_value
            remainder -= digit_value
            result += @@digits_lookup[digit_value]
          end

          break if remainder <= 0
        end
      end
    end
  end
end
