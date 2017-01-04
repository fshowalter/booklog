# frozen_string_literal: true
require 'inquirer'

module Booklog
  #
  # Namespace for movielog console use-cases.
  #
  module Console
    #
    # Responsible for providing a command-line interface to create new viewings.
    #
    class CreatePage
      class << self
        #
        # Responsible for processing a new viewing command.
        #
        # @return [String] The full path to the new entry.
        def call
          page = Booklog::CreatePage.call(title: ask_for_title)

          puts "\n Created Page #{Bold.call(text: page.title)}!\n"

          page
        end

        private

        def ask_for_title(title = nil)
          while title.nil?
            entered_title = Ask.input 'Page Title'
            title = entered_title if Ask.confirm entered_title
          end

          title
        end
      end
    end
  end
end
