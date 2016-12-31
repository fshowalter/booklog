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
    class CreateFeature
      class << self
        #
        # Responsible for processing a new viewing command.
        #
        # @return [String] The full path to the new entry.
        def call
          loop do
            feature_hash = { title: get_title, date: get_date }

            Movielog::App.create_feature(feature_hash)

            puts "\n Created Feature ##{bold(feature_hash[:number].to_s)}!\n" \
            " #{bold('        Title:')} #{feature_hash[:title]}\n" \
            " #{bold('         Date:')} #{feature_hash[:date]}\n"
          end
        end

        private

        def bold(text)
          term = Term::ANSIColor
          term.cyan text
        end

        #
        # Resposible for getting the date from the user.
        #
        # @param title [String] The chosen title.
        #
        # @return [String] The chosen title.
        def get_title(title = nil)
          while title.nil?
            entered_title = Ask.input 'Feature Title'
            title = entered_title if Ask.confirm entered_title
          end

          title
        end

        #
        # Resposible for getting the date from the user.
        #
        # @param terminal [HighLine] The current HighLine instance.
        #
        # @return [String] The entered date.
        def get_date(default = Date.today.to_s)
          date = nil

          while date.nil?
            entered_date = Ask.input 'Date', default: default
            next unless (entered_date = Date.parse(entered_date))

            date = entered_date if Ask.confirm entered_date.strftime('%A, %B %d, %Y?  ')
          end

          date
        end
      end
    end
  end
end
