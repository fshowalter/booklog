# frozen_string_literal: true
module Booklog
  #
  # Responsible for holding review data.
  #
  class Review
    extend Forwardable

    attr_reader :sequence, :date, :grade, :content, :cover, :cover_placeholder

    def initialize(sequence:, book:, date:, grade:, content:, cover: '', cover_placeholder: nil)
      @book = book
      @sequence = sequence
      @date = date
      @grade = grade
      @content = content
      @cover = cover
      @cover_placeholder = cover_placeholder
    end

    def_delegators :@book, :id, :title, :aka_titles, :title_with_author, :authors, :year_published, :isbn
  end
end
