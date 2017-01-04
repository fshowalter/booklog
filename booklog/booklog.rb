# frozen_string_literal: true
require 'active_support/core_ext/array/conversions'

Dir[File.expand_path('../**/*.rb', __FILE__)].each { |f| require f }

#
# Responsible for defining the Booklog API.
#
module Booklog
  class << self
    def site_url
      'https://booklog.frankshowalter.com'
    end

    def site_title
      "Frank's Book Log"
    end

    def site_tagline
      'Literature is a Relative Term'
    end

    def next_reading_number(readings: Booklog.readings)
      readings.length + 1
    end

    def next_review_number(reviews: Booklog.reviews)
      reviews.length + 1
    end

    def readings_path
      File.expand_path('../../readings/', __FILE__)
    end

    def reviews_path
      File.expand_path('../../reviews/', __FILE__)
    end

    def books_path
      File.expand_path('../../books/', __FILE__)
    end

    def pages_path
      File.expand_path('../../pages/', __FILE__)
    end

    def readings
      ParseReadings.call(readings_path: readings_path) || []
    end

    def reviews
      ParseReviews.call(reviews_path: reviews_path) || {}
    end

    def books
      ParseBooks.call(books_path: books_path) || {}
    end

    def reviews_by_sequence
      reviews.values.sort_by(&:sequence).reverse
    end

    def pages
      ParsePages.call(pages_path: pages_path) || {}
    end

    def authors
      reviews.values.each_with_object({}) do |review, memo|
        book = books[review.book_id]
        book.authors.each do |author|
          memo[author] ||= author
          memo[author].reviews[review.book_id] = review
        end
        memo
      end
    end

    def readings_for_book_id(readings: Booklog.readings, book_id:)
      readings.select { |reading| reading.book_id == book_id }
    end

    def create_page(feature_hash)
      feature_hash[:date] = Date.today
      feature_hash[:sequence] = posts.length + 1
      feature_hash[:slug] = Booklog::Slugize.call(text: feature_hash[:title])
      CreateFeature.call(features_path, feature_hash)
    end
  end
end
