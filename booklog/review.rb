# frozen_string_literal: true
module Booklog
  #
  # Responsible for holding review data.
  #
  class Review
    attr_reader :sequence, :book_id, :date, :grade, :content

    def initialize(sequence:, book_id:, date:, grade:, content:)
      @sequence = sequence
      @book_id = book_id
      @date = date
      @grade = grade
      @content = content
    end
  end
end
