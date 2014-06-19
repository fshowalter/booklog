require 'active_support/core_ext/object/try'
require 'active_support/core_ext/array/conversions'

module Booklog
  #
  # Namespace for booklog console use-cases.
  #
  module Console
    #
    # Responsible for providing a command-line interface to create new reviews.
    #
    class CreateReview
      class << self
        #
        # Responsible for processing a new review command.
        #
        # @return [String] The full path to the new entry.
        def call
          loop do
            review_hash = {
              title: get_title,
              authors: get_authors,
              page_count: get_page_count,
              year_published: get_year,
              date_started: get_date_started,
              date_finished: get_date_finished }

            file = Booklog::App.create_review(review_hash)

            puts "\n Created Review ##{bold(review_hash[:sequence].to_s)}!\n" \
            " #{bold('         Title:')} #{review_hash[:title]}\n" \
            " #{bold('       Authors:')} #{review_hash[:authors].to_sentence}\n" \
            " #{bold('    Page Count:')} #{review_hash[:page_count].to_s}\n" \
            " #{bold('Year Published:')} #{review_hash[:year_published].to_s}\n" \
            " #{bold('  Date Started:')} #{review_hash[:date_started]}\n" \
            " #{bold(' Date Finished:')} #{review_hash[:date_finished]}\n" \

            exec "open #{file}"
          end
        end

        private

        def bold(text)
          term = Term::ANSIColor
          term.cyan text
        end

        #
        # Resposible for getting the title from the user.
        #
        # @param title [String] The chosen title.
        #
        # @return [String] The chosen title.
        def get_title(title = nil)
          while title.nil?
            entered_title = Ask.input 'Book Title'
            title = entered_title if Ask.confirm entered_title
          end

          title
        end

        #
        # Resposible for getting the page count from the user.
        #
        # @param page_count [String] The default page count.
        #
        # @return [String] The chosen title.
        def get_page_count(page_count = nil)
          while page_count.nil?
            entered_page_count = Ask.input 'Page Count'
            page_count = entered_page_count if Ask.confirm entered_page_count
          end

          page_count
        end

        #
        # Resposible for getting the page count from the user.
        #
        # @param year [String] The default page count.
        #
        # @return [String] The chosen title.
        def get_year(year = nil)
          while year.nil?
            entered_year = Ask.input 'Year Published'
            year = entered_year if Ask.confirm entered_year
          end

          year
        end

        #
        # Resposible for getting the authors from the user.
        #
        # @param authors [Enumerable<String>] The default authors.
        #
        # @return [Enumerable<String>] The entered authors.
        def get_authors(authors = [])
          add_authors = true

          while add_authors
            author = Ask.input 'Author'
            authors << author if Ask.confirm author
            add_authors = Ask.confirm 'Add More Authors'
          end

          authors
        end

        #
        # Resposible for getting the start date from the user.
        #
        # @param date [Date] The default date.
        #
        # @return [String] The entered date.
        def get_date_started(date = nil)
          last_date = Booklog::App.reviews[Booklog::App.reviews.length]
          default = last_date.try(:[], :date_finished).to_s

          while date.nil?
            entered_date = Ask.input 'Date Started', default: default
            next unless (entered_date = Date.parse(entered_date))

            date = entered_date if Ask.confirm entered_date.strftime('%A, %B %d, %Y?  ')
          end

          date
        end

        #
        # Resposible for getting the date from the user.
        #
        # @param default [Date] The default date.
        #
        # @return [String] The entered date.
        def get_date_finished(default = Date.today.to_s)
          date = nil

          while date.nil?
            entered_date = Ask.input 'Date Finished', default: default
            next unless (entered_date = Date.parse(entered_date))

            date = entered_date if Ask.confirm entered_date.strftime('%A, %B %d, %Y?  ')
          end

          date
        end
      end
    end
  end
end
