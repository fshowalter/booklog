# frozen_string_literal: true
require 'active_support/core_ext/array/conversions'

Dir[File.expand_path('../**/*.rb', __FILE__)].each { |f| require f }

#
# Responsible for defining the Booklog API.
#
module Booklog
  class << self
    attr_accessor :cache_reviews

    def site_url
      'https://booklog.frankshowalter.com'
    end

    def site_title
      "Frank's Book Log"
    end

    def site_tagline
      'Literature is a Relative Term'
    end

    def next_reading_sequence(readings: Booklog.readings)
      readings.length + 1
    end

    def next_review_sequence(reviews: Booklog.reviews)
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

    def readings(readings_path: Booklog.readings_path)
      @readings ||= ParseReadings.call(readings_path: readings_path) || []
    end

    def reviews(reviews_path: Booklog.reviews_path)
      if cache_reviews
        @reviews ||= ParseReviews.call(reviews_path: reviews_path) || {}
      else
        ParseReviews.call(reviews_path: reviews_path) || {}
      end
    end

    def books(books_path: Booklog.books_path)
      @books ||= ParseBooks.call(books_path: books_path) || {}
    end

    def reviews_by_sequence(reviews: Booklog.reviews)
      if cache_reviews
        @reviews_by_sequence ||= reviews.values.sort_by(&:sequence).reverse
      else
        reviews.values.sort_by(&:sequence).reverse
      end
    end

    def pages(pages_path: Booklog.pages_path)
      @pages ||= ParsePages.call(pages_path: pages_path) || {}
    end

    def authors(reviews: Booklog.reviews, books: Booklog.books)
      @authors ||= reviews.values.map do |review|
        books[review.isbn].authors
      end.flatten.uniq(&:slug)
    end

    def readings_for_isbn(readings: Booklog.readings, isbn:)
      readings.select { |reading| reading.isbn == isbn }
    end
  end
end
