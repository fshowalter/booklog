# frozen_string_literal: true
module Booklog
  #
  # Responsible for holding review data.
  #
  class Reading
    extend Forwardable

    attr_reader :sequence, :book_id, :isbn, :pages_total, :pages_read, :date_started, :date_finished

    def initialize(sequence:, book:, isbn:, pages_total:, pages_read:, date_started:, date_finished:)
      @sequence = sequence
      @book = book
      @book_id = book.id
      @isbn = isbn
      @pages_total = pages_total
      @pages_read = pages_read
      @date_started = date_started
      @date_finished = date_finished
    end

    def_delegators :@book, :title, :sortable_title, :title_with_author, :authors, :year_published
  end
end
