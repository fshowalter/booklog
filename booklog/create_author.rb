# frozen_string_literal: true
module Booklog
  #
  # Responsible for creating new author instances.
  #
  class CreateAuthor
    class << self
      DIGITS = {
        'I' => 1,
        'V' => 5,
        'X' => 10,
        'L' => 50,
        'C' => 100,
        'D' => 500,
        'M' => 1000
      }.freeze

      @digits_lookup = DIGITS.inject(
        4 => 'IV',
        9 => 'IX',
        40 => 'XL',
        90 => 'XC',
        400 => 'CD',
        900 => 'CM'
      ) { |memo, pair| memo.update(pair.last => pair.first) }

      def call(authors_path: Booklog.authors_path, authors: Booklog.authors, name:, sortable_name:, url:)
        name_with_annotation = add_annotation(name: name, authors: authors)
        id = build_id(name_with_annotation: name_with_annotation)
        file_name = File.join(authors_path, id + '.yml')

        front_matter = {
          id: id,
          name: name.strip,
          name_with_annotation: name_with_annotation,
          sortable_name: sortable_name.strip,
          url: url.strip
        }

        content = "#{front_matter.to_yaml}\n"

        File.open(file_name, 'w') { |file| file.write(content) }

        OpenStruct.new(front_matter)
      end

      private

      def add_annotation(name:, authors:)
        name_with_annotation = name.strip
        existing_authors = authors.values.select { |a| a.name == name_with_annotation }

        if existing_authors.any?
          name_with_annotation = "#{name_with_annotation} (#{to_roman(existing_authors.length + 1)})"
        end

        name_with_annotation
      end

      def build_id(name_with_annotation:)
        Booklog::Slugize.call(text: name_with_annotation)
      end

      def to_roman(int)
        raise if int.negative? || int > 3999
        remainder = int
        result = ''

        @digits_lookup.keys.sort.reverse.each do |digit_value|
          while remainder >= digit_value
            remainder -= digit_value
            result += @@digits_lookup[digit_value]
          end

          break if remainder <= 0
        end

        result
      end
    end
  end
end
