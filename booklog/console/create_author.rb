# frozen_string_literal: true
require 'inquirer'
require 'awesome_print'

module Booklog
  module Console
    #
    # Responsible for providing a console interface to create new authors.
    #
    class CreateAuthor
      class << self
        #
        # Responsible for processing a new author command.
        #
        # @return [Hash] The new author.
        def call
          author = Booklog::CreateAuthor.call(**build_author_data)

          puts "\n Created Author ##{Bold.call(text: author.id)}!\n"

          ap(author.to_h, ruby19_syntax: true)

          author
        end

        private

        def build_author_data
          name = ask_for_name

          {
            name: name,
            sortable_name: ask_for_sortable_name(name: name),
            url: ask_for_url
          }
        end

        def ask_for_name
          name = nil

          while name.nil?
            entered_name = Ask.input 'Name'
            name = entered_name if Ask.confirm entered_name
          end

          name
        end

        def ask_for_sortable_name(name:)
          sortable_name = nil

          while sortable_name.nil?
            entered_name = Ask.input 'Sortable Name', default: build_default_sortable_name(name)
            sortable_name = entered_name if Ask.confirm entered_name
          end

          sortable_name
        end

        def ask_for_url
          url = nil

          while url.nil?
            entered_url = Ask.input 'URL'
            url = entered_url if Ask.confirm entered_url
          end

          url
        end

        def build_default_sortable_name(name)
          first_name, _, last_name = name.rpartition(' ')

          "#{last_name}, #{first_name}"
        end
      end
    end
  end
end
