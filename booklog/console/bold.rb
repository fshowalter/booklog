# frozen_string_literal: true
module Booklog
  module Console
    #
    # Responsible for formatting as bold for the console.
    #
    class Bold
      class << self
        def call(text:)
          term = Term::ANSIColor
          term.cyan text
        end
      end
    end
  end
end
