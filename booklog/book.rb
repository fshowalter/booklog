# frozen_string_literal: true

module Booklog
  #
  # Responsible for holding review data.
  #
  class Book
    attr_reader :id, :title, :aka_titles, :authors, :page_count, :year_published, :isbn

    def initialize(id:, title:, aka_titles:, authors:, page_count:, year_published:, isbn:)
      @id = id
      @title = title
      @aka_titles = aka_titles
      @authors = authors
      @page_count = page_count
      @year_published = year_published
      @isbn = isbn
    end
  end
end
