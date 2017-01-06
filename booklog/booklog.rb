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

    def authors_path
      File.expand_path('../../authors/', __FILE__)
    end

    def readings(readings_path: Booklog.readings_path, books: Booklog.books)
      @readings ||= ParseReadings.call(readings_path: readings_path, books: books) || []
    end

    def reviews(reviews_path: Booklog.reviews_path, books: Booklog.books)
      if cache_reviews
        @reviews ||= ParseReviews.call(reviews_path: reviews_path, books: books) || {}
      else
        ParseReviews.call(reviews_path: reviews_path, books: books) || {}
      end
    end

    def books(books_path: Booklog.books_path, authors: Booklog.authors)
      @books ||= ParseBooks.call(books_path: books_path, authors: authors) || {}
    end

    def reviews_by_sequence(reviews: Booklog.reviews)
      if cache_reviews
        @reviews_by_sequence ||= reviews.values.sort_by(&:sequence).reverse
      else
        reviews.values.sort_by(&:sequence).reverse
      end
    end

    def reviews_by_author(reviews: Booklog.reviews)
      if cache_reviews
        @reviews_by_author ||= reviews.values.each_with_object({}) do |review, memo|
          review.authors.each do |author|
            memo[author.id] ||= []
            memo[author.id] << review
          end
        end
      else
        reviews.values.each_with_object({}) do |review, memo|
          review.authors.each do |author|
            memo[author.id] ||= []
            memo[author.id] << review
          end
        end
      end
    end

    def pages(pages_path: Booklog.pages_path)
      @pages ||= ParsePages.call(pages_path: pages_path) || {}
    end

    def authors(authors_path: Booklog.authors_path)
      @authors ||= ParseAuthors.call(authors_path: authors_path) || {}
    end

    def readings_for_book_id(readings: Booklog.readings, book_id:)
      readings.select { |reading| reading.book_id == book_id }
    end
  end
end
