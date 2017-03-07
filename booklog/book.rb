# frozen_string_literal: true

module Booklog
  #
  # Responsible for holding book data.
  #
  class Book
    attr_reader :id, :title, :title_with_author, :isbn, :sortable_title, :aka_titles, :year_published, :authors, :publisher, :pages_total

    def initialize(id:, title:, aka_titles:, isbn:, authors:, year_published:, sortable_title:, publisher: nil, pages_total: 0)
      @id = id
      @title = title
      @title_with_author = "#{title} by #{authors.map(&:name).to_sentence}"
      @aka_titles = aka_titles
      @year_published = year_published
      @authors = authors
      @isbn = isbn
      @sortable_title = sortable_title
      @publisher = publisher
      @pages_total = pages_total
    end
  end
end
