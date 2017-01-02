# frozen_string_literal: true

module Booklog
  #
  # Responsible for holding review data.
  #
  class Book
    attr_reader :id, :title, :aka_titles, :authors, :page_count, :year_published, :isbn, :cover, :cover_placeholder

    def initialize(id:, title:, aka_titles:, authors:, page_count:, year_published:, isbn:, cover: '', cover_placeholder: nil)
      @id = id
      @title = title
      @aka_titles = aka_titles
      @authors = authors.map { |sortable_name| Author.new(sortable_name: sortable_name) }
      @page_count = page_count
      @year_published = year_published
      @isbn = isbn
      @cover = cover
      @cover_placeholder = cover_placeholder
    end

    def title_with_author
      "#{title} by #{authors.map(&:name).to_sentence}"
    end

    def sortable_title
      @sortable_title_regex ||= Regexp.new("^('|(?:[Tt]he|[Aa]n?)\\s)")

      if (sortable_match = @sortable_title_regex.match(title))
        sortable_match.post_match + ", #{sortable_match[1].strip}"
      else
        title
      end
    end
  end
end
