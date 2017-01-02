# frozen_string_literal: true
module Booklog
  class Author
    attr_reader :name, :sortable_name, :reviews, :slug, :last_name, :first_name, :annotation

    def initialize(sortable_name:)
      @sortable_name = sortable_name
      @reviews = {}

      name_match = name_regex.match(sortable_name)
      @last_name = name_match[1]
      @first_name = name_match[2]
      @annotation = name_match[3]
      @name = "#{first_name} #{last_name}"
      @slug = Booklog::Slugize.call(text: "#{name} #{annotation}")
    end

    private

    def name_regex
      @name_regex ||= Regexp.new(
        # from the beginning of the line capture everything up to a tab or comma
        '^([^(\t,]*)' +
        # followed by an optional comma
        ',?' +
        # then optionally capture anything up to an open paren or tab
        '([^\t(]*)?' +
        # then optionally capture everything between two parens that isn't a whitespace
        '(?:[(]([^\s)]*)[)])?'
      )
    end
  end
end
