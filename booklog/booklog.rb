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

    def next_reading_number
      readings.length + 1
    end

    def next_review_number
      reviews.length + 1
    end

    def next_post_number
      (reviews.length + pages.length) + 1
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
      ParseReadings.call(readings_path: readings_path) || {}
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
      reviews.each_with_object({}) do |(_sequence, review), memo|
        review.authors.each do |author|
          memo[author] ||= Author.new(name: author)
          memo[author].slug ||= slugize(author)
          memo[author].titles ||= {}
          memo[author].titles[review.title] = review
        end
        memo
      end
    end

    def info_for_book(id:)
      books[id]
    end

    def readings_for_id(id:)
      readings.values.select { |reading| reading.book_id == id }
    end

    def create_page(feature_hash)
      feature_hash[:date] = Date.today
      feature_hash[:sequence] = posts.length + 1
      feature_hash[:slug] = slugize(feature_hash[:title])
      CreateFeature.call(features_path, feature_hash)
    end

    private

    def slugize(words, slug = '-')
      slugged = words.encode('UTF-8', invalid: :replace, undef: :replace, replace: '?')
      slugged.gsub!(/&/, 'and')
      slugged.delete!(':')
      slugged.gsub!(/[^\w_\-#{Regexp.escape(slug)}]+/i, slug)
      slugged.gsub!(/#{slug}{2,}/i, slug)
      slugged.gsub!(/^#{slug}|#{slug}$/i, '')
      url_encode(slugged.downcase)
    end

    def url_encode(word)
      URI.escape(word, /[^\w_+-]/i)
    end
  end
end
