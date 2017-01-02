# frozen_string_literal: true
module Booklog
  #
  # Responsible for holding review data.
  #
  class Reading
    attr_reader :sequence, :book_id, :pages_read, :date_started, :date_finished

    def initialize(sequence:, book_id:, pages_read:, date_started:, date_finished:)
      @sequence = sequence
      @book_id = book_id
      @pages_read = pages_read
      @date_started = date_started
      @date_finished = date_finished
    end
  end
end
